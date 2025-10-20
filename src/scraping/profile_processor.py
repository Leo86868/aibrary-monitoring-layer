"""
AIbrary TikTok Monitoring System - Profile Processor
Processor for TikTok user profiles (@username)
"""

import time
import re
import requests
from typing import List, Optional
from datetime import datetime, timedelta

from core import MonitoringTarget, TikTokContent, ProcessingResult, APIFY_TOKEN, TIKTOK_ACTOR_ID, DEFAULT_TIMEOUT
from .base import BaseProcessor


class ProfileProcessor(BaseProcessor):
    """Processor for TikTok user profiles (@username)"""

    def __init__(self):
        if not APIFY_TOKEN:
            raise ValueError("APIFY_TOKEN environment variable is required")
        self.token = APIFY_TOKEN.strip()

    def can_process(self, target: MonitoringTarget) -> bool:
        """Check if this is a profile target"""
        return target.is_profile and target.platform == "tiktok"

    def process(self, target: MonitoringTarget, use_cached_data: bool = True) -> ProcessingResult:
        """Process TikTok profile target using synchronous HTTP API or cached data"""
        start_time = time.time()

        try:
            print(f"🎯 Processing profile: {target.target_value}")

            # Try to get recent data first if use_cached_data is True
            dataset_items = None
            if use_cached_data:
                dataset_items = self._get_recent_run_data(target)

            # If no recent data found, run the actor
            if not dataset_items:
                print(f"🚀 Running Apify actor for fresh data...")
                # Prepare Apify input
                run_input = self._prepare_apify_input(target)

                # Use direct HTTP API for synchronous run with dataset items
                url = f"https://api.apify.com/v2/acts/{TIKTOK_ACTOR_ID}/run-sync-get-dataset-items"

                response = requests.post(
                    url,
                    params={"token": self.token},
                    json=run_input,
                    timeout=DEFAULT_TIMEOUT
                )
                response.raise_for_status()
                dataset_items = response.json()
            else:
                print(f"📄 Using cached data from recent run")

            # Process results directly from dataset items
            content_list = self._process_dataset_items(dataset_items, target)

            processing_time = time.time() - start_time
            print(f"✅ Profile {target.target_value}: Found {len(content_list)} videos in {processing_time:.1f}s")

            return self._create_success_result(target, content_list, processing_time)

        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Failed to process profile {target.target_value}: {str(e)}"
            print(f"❌ {error_msg}")
            return self._create_error_result(target, error_msg, processing_time)

    def _prepare_apify_input(self, target: MonitoringTarget) -> dict:
        """Prepare input configuration for Apify TikTok scraper"""
        username = target.target_value.lstrip('@')

        return {
            "profiles": [f"@{username}"],
            "resultsPerPage": target.results_limit,
            "profileScrapeSections": ["videos"],  # Only scrape videos section
            "shouldDownloadVideos": True,  # Download videos for AI analysis
            "shouldDownloadCovers": True,  # Download thumbnails for visual reference
            "shouldDownloadSubtitles": True,  # Download subtitles to avoid needing Whisper transcription
            "shouldDownloadSlideshowImages": False,  # Filter out photo carousels, only get actual videos
            "proxyConfiguration": {"useApifyProxy": True}
        }

    def _process_dataset_items(self, dataset_items, target: MonitoringTarget) -> List[TikTokContent]:
        """Process dataset items directly into TikTokContent objects"""
        content_list = []
        slideshow_count = 0

        for item in dataset_items:
            try:
                # Filter out photo slideshows - only process actual videos
                if item.get("isSlideshow", False):
                    slideshow_count += 1
                    continue

                content = self._convert_item_to_content(item, target)
                if content:
                    content_list.append(content)
            except Exception as e:
                print(f"⚠️ Failed to process item: {e}")
                continue

        if slideshow_count > 0:
            print(f"   ⏭️ Filtered out {slideshow_count} photo slideshow(s)")

        return content_list

    def _convert_item_to_content(self, item: dict, target: MonitoringTarget) -> TikTokContent:
        """Convert Apify result item to TikTokContent"""
        content_id = item.get("id") or item.get("videoId") or self._extract_video_id(item.get("webVideoUrl", ""))

        if not content_id:
            raise ValueError("No content ID found")

        # Extract real data from Apify response
        video_url = item.get("webVideoUrl", "")
        caption = item.get("text", "")[:500] if item.get("text") else ""

        # Get author info from authorMeta
        author_meta = item.get("authorMeta", {})
        author_username = author_meta.get("name", "")
        if author_username:
            author_username = author_username.lstrip('@')

        # Extract video download URLs and media data from actual response structure
        video_meta = item.get("videoMeta", {})

        # Get the downloaded video URL (watermark-free version) from mediaUrls array
        media_urls = item.get("mediaUrls", [])
        video_download_url = media_urls[0] if media_urls else ""

        # Debug: Print what we got
        print(f"   🔍 DEBUG - Content {content_id}:")
        print(f"      mediaUrls: {media_urls}")
        print(f"      video_download_url: {video_download_url}")

        # Get subtitle URL from videoMeta.subtitleLinks (first English or available language)
        subtitle_links = video_meta.get("subtitleLinks", [])
        subtitle_url = ""
        if subtitle_links:
            # Try to find English first, otherwise take the first available
            for subtitle in subtitle_links:
                if subtitle.get("language") == "eng" or "en" in subtitle.get("language", "").lower():
                    subtitle_url = subtitle.get("downloadLink", "")
                    break
            # If no English found, take the first available
            if not subtitle_url and subtitle_links:
                subtitle_url = subtitle_links[0].get("downloadLink", "")

        # Extract engagement metrics from Apify response
        likes = item.get("diggCount", 0)
        comments = item.get("commentCount", 0)
        views = item.get("playCount", 0)

        # Parse the numbers (they might be strings with K/M notation)
        likes = self._parse_number(likes)
        comments = self._parse_number(comments)
        views = self._parse_number(views)

        content = TikTokContent(
            content_id=str(content_id),
            target_value=target.target_value,
            video_url=video_url,
            author_username=author_username,
            caption=caption,
            likes=likes,
            comments=comments,
            views=views,
            engagement_rate=0.0  # Will be calculated when saving
        )

        # Store additional media URLs as attributes (will be saved to database)
        content.video_download_url = video_download_url
        content.subtitle_url = subtitle_url

        return content

    def _extract_video_id(self, video_url: str) -> str:
        """Extract video ID from TikTok URL"""
        if not video_url:
            return ""

        match = re.search(r'/video/(\d+)', video_url)
        if match:
            return match.group(1)

        return video_url.split('/')[-1] if '/' in video_url else video_url

    def _get_recent_run_data(self, target: MonitoringTarget) -> Optional[list]:
        """Get data from the most recent Apify run instead of running a new one"""
        try:
            # Get list of recent runs for this actor
            runs_url = f"https://api.apify.com/v2/acts/{TIKTOK_ACTOR_ID}/runs"

            response = requests.get(
                runs_url,
                params={"token": self.token, "limit": 10, "status": "SUCCEEDED"},
                timeout=30
            )
            response.raise_for_status()
            runs_data = response.json()

            # Find the most recent successful run
            if not runs_data.get("data", {}).get("items"):
                return None

            # Get the most recent run
            recent_run = runs_data["data"]["items"][0]
            run_id = recent_run["id"]

            # Check if it's recent enough (within last hour)
            run_time = datetime.fromisoformat(recent_run["finishedAt"].replace('Z', '+00:00'))
            if datetime.now().astimezone() - run_time > timedelta(hours=1):
                print(f"⏰ Most recent run is {run_time}, too old - will run fresh actor")
                return None

            print(f"📊 Found recent run from {run_time.strftime('%H:%M:%S')}, getting dataset...")

            # Get dataset items from the recent run
            dataset_url = f"https://api.apify.com/v2/acts/{TIKTOK_ACTOR_ID}/runs/{run_id}/dataset/items"

            response = requests.get(
                dataset_url,
                params={"token": self.token},
                timeout=60
            )
            response.raise_for_status()

            dataset_items = response.json()

            # Filter for the specific profile we want
            username = target.target_value.lstrip('@')
            filtered_items = []

            for item in dataset_items:
                # Check if this item is from our target profile
                author_meta = item.get("authorMeta", {})
                if author_meta.get("name", "").lower() == username.lower():
                    filtered_items.append(item)

            if filtered_items:
                print(f"✅ Found {len(filtered_items)} items for {target.target_value} in recent run")
                return filtered_items[:target.results_limit]  # Limit to requested amount
            else:
                print(f"⚠️ No items found for {target.target_value} in recent run")
                return None

        except Exception as e:
            print(f"⚠️ Failed to get recent run data: {e}")
            return None

    def _parse_number(self, value) -> int:
        """Parse number from various formats"""
        if isinstance(value, int):
            return value

        if isinstance(value, str):
            value = value.upper().replace(',', '')

            if 'K' in value:
                return int(float(value.replace('K', '')) * 1000)
            elif 'M' in value:
                return int(float(value.replace('M', '')) * 1000000)
            elif 'B' in value:
                return int(float(value.replace('B', '')) * 1000000000)
            else:
                try:
                    return int(value)
                except ValueError:
                    return 0

        return 0
