"""
AIbrary TikTok Monitoring System - Video Analyzer
Main AI analysis engine for TikTok content

Current Implementation:
- Uses COMPETITOR_INTELLIGENCE_PROMPT for all content
- Optimized for Competitor Intelligence monitoring strategy

Future Enhancement:
- Add prompt routing based on content.monitoring_strategy field
- STRATEGY_PROMPTS = {
    "competitor_intelligence": COMPETITOR_INTELLIGENCE_PROMPT,
    "trend_discovery": TREND_DISCOVERY_PROMPT,  # future
    "niche_deepdive": NICHE_DEEPDIVE_PROMPT,    # future
  }
"""

import requests
import tempfile
import os
from typing import Optional, List, Dict, Any
import google.generativeai as genai

from core import TikTokContent, GEMINI_API_KEY
from core.models import AnalysisResult
from .prompts import COMPETITOR_INTELLIGENCE_PROMPT, NICHE_DEEPDIVE_PROMPT, VIDEO_ANALYSIS_PROMPT
from .parsers import (
    parse_competitor_intelligence_response,
    parse_niche_deepdive_response,
    parse_general_analysis_response,
    parse_subtitle_content
)


class VideoAnalyzer:
    """Handles AI analysis of TikTok videos"""

    def __init__(self):
        """Initialize the video analyzer with API credentials"""
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            print("⚠️ GEMINI_API_KEY not found - AI analysis disabled")

    def analyze_content(self, content: TikTokContent, analysis_type: str = "competitor_intelligence") -> Optional[AnalysisResult]:
        """
        Analyze TikTok content using available data based on monitoring strategy
        Priority: Subtitles > Video > Caption only

        Routes to strategy-specific analysis based on content.monitoring_strategy field:
        - "Competitor Intelligence" → Analyze with competitor intelligence prompt
        - "Trend Discovery" → Skip (prompt not implemented yet)
        - "Niche Deep-Dive" → Skip (prompt not implemented yet)
        - None/Unknown → Skip with warning
        """
        if not self.model:
            return None

        try:
            # Get monitoring strategy from content (populated via Lark Base lookup)
            strategy = content.monitoring_strategy

            # Route based on monitoring strategy
            if strategy == "Competitor Intelligence":
                return self._analyze_competitor_intelligence(content)
            elif strategy == "Trend Discovery":
                print(f"   ⏭️  {content.content_id} (Trend Discovery) - skipping (prompt not implemented)")
                return None
            elif strategy == "Niche Deep-Dive":
                return self._analyze_niche_deepdive(content)
            elif strategy is None or strategy == "":
                print(f"   ⚠️  {content.content_id} - No monitoring strategy, skipping analysis")
                return None
            else:
                print(f"   ⚠️  {content.content_id} - Unknown strategy '{strategy}', skipping")
                return None

        except Exception as e:
            print(f"❌ AI analysis failed for {content.content_id}: {e}")
            return None

    def _analyze_competitor_intelligence(self, content: TikTokContent) -> Optional[AnalysisResult]:
        """Analyze content specifically for competitor intelligence insights"""

        # Get subtitle text if available
        subtitles = ""
        if content.subtitle_url:
            subtitles = self._fetch_subtitles(content.subtitle_url)

        # Try to download and analyze video if available
        video_file = None
        video_available = False

        if content.video_download_url:
            print(f"   📥 Downloading video from {content.video_download_url[:60]}...")
            video_file = self._download_video(content.video_download_url, content.content_id)
            if video_file:
                print(f"   ✅ Video downloaded: {video_file}")
                video_available = True
            else:
                print(f"   ⚠️ Video download failed, falling back to text-only analysis")

        try:
            # Format the competitor intelligence prompt
            prompt_text = COMPETITOR_INTELLIGENCE_PROMPT.format(
                author_username=content.author_username or "Unknown",
                caption=content.caption or "No caption provided",
                subtitles=subtitles or "No subtitles available",
                likes=content.likes or 0,
                comments=content.comments or 0,
                views=content.views or 0
            )

            # Add video analysis context to prompt
            if video_available:
                prompt_text = f"""You are analyzing a TikTok VIDEO (visual + audio content).

Pay attention to:
- Visual presentation and editing style
- On-screen text and graphics
- Speaker delivery and energy
- Production quality and professionalism
- Visual storytelling techniques

{prompt_text}"""

            # Generate analysis with video if available
            if video_available and video_file:
                print(f"   📤 Uploading video to Gemini...")
                # Read video file as bytes
                with open(video_file, 'rb') as f:
                    video_data = f.read()

                print(f"   🎬 Analyzing video with AI (this may take 60-90 seconds)...")
                # Use Part API for inline video data
                video_part = {"mime_type": "video/mp4", "data": video_data}
                response = self.model.generate_content([video_part, prompt_text])
            else:
                # Text-only analysis
                print(f"   📝 Analyzing text only...")
                response = self.model.generate_content(prompt_text)

            # Parse and structure the response for competitor intelligence
            result = parse_competitor_intelligence_response(content.content_id, response.text)

            return result

        finally:
            # Clean up temporary video file
            if video_file and os.path.exists(video_file):
                try:
                    os.remove(video_file)
                    print(f"   🗑️ Cleaned up temporary video file")
                except Exception as e:
                    print(f"   ⚠️ Failed to cleanup video file: {e}")

    def _analyze_niche_deepdive(self, content: TikTokContent) -> Optional[AnalysisResult]:
        """Analyze content for niche deep-dive insights (content strategies from adjacent niches)"""

        # Get subtitle text if available
        subtitles = ""
        if content.subtitle_url:
            subtitles = self._fetch_subtitles(content.subtitle_url)

        # Try to download and analyze video if available
        video_file = None
        video_available = False

        if content.video_download_url:
            print(f"   📥 Downloading video from {content.video_download_url[:60]}...")
            video_file = self._download_video(content.video_download_url, content.content_id)
            if video_file:
                print(f"   ✅ Video downloaded: {video_file}")
                video_available = True
            else:
                print(f"   ⚠️ Video download failed, falling back to text-only analysis")

        try:
            # Format the niche deep-dive prompt
            prompt_text = NICHE_DEEPDIVE_PROMPT.format(
                author_username=content.author_username or "Unknown",
                caption=content.caption or "No caption provided",
                subtitles=subtitles or "No subtitles available",
                likes=content.likes or 0,
                comments=content.comments or 0,
                views=content.views or 0
            )

            # Add video analysis context to prompt
            if video_available:
                prompt_text = f"""You are analyzing a TikTok VIDEO (visual + audio content).

Pay attention to:
- Visual presentation and editing style
- On-screen text and graphics
- Speaker delivery and energy
- Content strategy techniques (hooks, format, engagement tactics)
- Trending topics and themes in this niche space

{prompt_text}"""

            # Generate analysis with video if available
            if video_available and video_file:
                print(f"   📤 Uploading video to Gemini...")
                # Read video file as bytes
                with open(video_file, 'rb') as f:
                    video_data = f.read()

                print(f"   🎬 Analyzing video with AI (this may take 60-90 seconds)...")
                # Use Part API for inline video data
                video_part = {"mime_type": "video/mp4", "data": video_data}
                response = self.model.generate_content([video_part, prompt_text])
            else:
                # Text-only analysis
                print(f"   📝 Analyzing text only...")
                response = self.model.generate_content(prompt_text)

            # Parse and structure the response for niche deep-dive
            result = parse_niche_deepdive_response(content.content_id, response.text)

            return result

        finally:
            # Clean up temporary video file
            if video_file and os.path.exists(video_file):
                try:
                    os.remove(video_file)
                    print(f"   🗑️ Cleaned up temporary video file")
                except Exception as e:
                    print(f"   ⚠️ Failed to cleanup video file: {e}")

    def _analyze_general(self, content: TikTokContent) -> Optional[AnalysisResult]:
        """Legacy general analysis method"""
        # Prepare analysis data
        analysis_input = self._prepare_analysis_input(content)

        # Generate analysis using Gemini
        response = self.model.generate_content(analysis_input)

        # Parse and structure the response
        result = parse_general_analysis_response(content.content_id, response.text)

        return result

    def _prepare_analysis_input(self, content: TikTokContent) -> str:
        """Prepare the input prompt for AI analysis"""

        # Get subtitle text if available
        subtitles = ""
        if content.subtitle_url:
            subtitles = self._fetch_subtitles(content.subtitle_url)

        # Format the analysis prompt
        prompt = VIDEO_ANALYSIS_PROMPT.format(
            caption=content.caption or "No caption provided",
            subtitles=subtitles or "No subtitles available"
        )

        return prompt

    def _fetch_subtitles(self, subtitle_url: str) -> str:
        """Fetch subtitle text from URL"""
        try:
            if subtitle_url:
                response = requests.get(subtitle_url, timeout=10)
                if response.status_code == 200:
                    # Parse subtitle format (SRT, VTT, etc.)
                    return parse_subtitle_content(response.text)
        except Exception as e:
            print(f"⚠️ Failed to fetch subtitles: {e}")

        return ""

    def _download_video(self, video_url: str, content_id: str) -> Optional[str]:
        """
        Download video to temporary file for AI analysis
        Returns: Path to temporary video file, or None if download fails
        """
        try:
            # Download video with streaming
            response = requests.get(video_url, stream=True, timeout=30)
            if response.status_code != 200:
                return None

            # Create temporary file
            suffix = '.mp4'  # Default to mp4
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
                prefix=f'tiktok_{content_id}_'
            )

            # Write video content
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)

            temp_file.close()
            return temp_file.name

        except Exception as e:
            print(f"   ❌ Video download error: {e}")
            return None

    def batch_analyze(self, content_list: List[TikTokContent], analysis_type: str = "competitor_intelligence") -> List[AnalysisResult]:
        """
        Analyze multiple content items with strategy-aware routing
        Tracks and reports metrics by monitoring strategy
        """
        results = []

        # Track counts by strategy
        strategy_counts = {
            "Competitor Intelligence": {"analyzed": 0, "skipped": 0},
            "Trend Discovery": {"analyzed": 0, "skipped": 0},
            "Niche Deep-Dive": {"analyzed": 0, "skipped": 0},
            "Unknown": {"analyzed": 0, "skipped": 0}
        }

        for content in content_list:
            strategy = content.monitoring_strategy or "Unknown"
            strategy_label = strategy if strategy in strategy_counts else "Unknown"

            print(f"🤖 Analyzing {content.content_id} ({strategy_label})...")
            result = self.analyze_content(content, analysis_type)

            if result:
                results.append(result)
                strategy_counts[strategy_label]["analyzed"] += 1
                # Update content with analysis results
                self._update_content_with_analysis(content, result)
            else:
                strategy_counts[strategy_label]["skipped"] += 1

        # Print summary report
        print(f"\n📊 Analysis complete:")
        total_analyzed = sum(s["analyzed"] for s in strategy_counts.values())
        total_skipped = sum(s["skipped"] for s in strategy_counts.values())

        for strategy_name, counts in strategy_counts.items():
            if counts["analyzed"] > 0:
                print(f"   ✅ {strategy_name}: {counts['analyzed']} analyzed")
            if counts["skipped"] > 0:
                status = "⏭️ " if strategy_name in ["Trend Discovery", "Niche Deep-Dive"] else "⚠️ "
                reason = "(awaiting prompt)" if strategy_name in ["Trend Discovery", "Niche Deep-Dive"] else "(no strategy)"
                print(f"   {status}{strategy_name}: {counts['skipped']} skipped {reason}")

        print(f"   📈 Total: {total_analyzed} analyzed, {total_skipped} skipped")

        return results

    def _update_content_with_analysis(self, content: TikTokContent, result: AnalysisResult):
        """Update TikTokContent object with two-stage analysis results"""

        # Update general analysis field (Stage 1) - for "Analysis" column in database
        content.ai_analysis_result = result.general_analysis if hasattr(result, 'general_analysis') else result.summary
        content.video_analyzed = True

        # Update strategic analysis fields (Stage 2) - for strategic columns in database
        content.strategic_score = result.strategic_score
        content.strategic_insights = result.strategic_insights

        # For Niche Deep-Dive, result.content_type contains niche_category
        if content.monitoring_strategy == "Niche Deep-Dive":
            content.niche_category = result.content_type
            content.content_type = None  # Don't set content_type for Niche Deep-Dive
        else:
            content.content_type = result.content_type


# ==============================================================================
# ANALYSIS UTILITIES
# ==============================================================================

def should_analyze_content(content: TikTokContent, min_engagement_rate: float = 5.0) -> bool:
    """
    Determine if content should be analyzed based on criteria
    Can be customized for selective processing to manage costs
    """

    # Skip if already analyzed
    if content.video_analyzed:
        return False

    # Analyze high-engagement content
    if content.engagement_rate >= min_engagement_rate:
        return True

    # Analyze if has significant views
    if content.views > 10000:
        return True

    # Skip low-engagement content to save costs
    return False


def analyze_new_content(content_list: List[TikTokContent]) -> Dict[str, Any]:
    """
    Main entry point for analyzing new TikTok content
    Returns analysis results and statistics
    """

    analyzer = VideoAnalyzer()

    # Filter content for analysis
    to_analyze = [c for c in content_list if should_analyze_content(c)]

    print(f"🎬 Analyzing {len(to_analyze)} of {len(content_list)} content items")

    # Perform analysis
    results = analyzer.batch_analyze(to_analyze)

    # Prepare summary
    summary = {
        "total_content": len(content_list),
        "analyzed": len(results),
        "skipped": len(content_list) - len(to_analyze),
        "results": results,
        "categories": {},
        "sentiments": {},
        "avg_viral_score": 0
    }

    # Aggregate statistics
    if results:
        for result in results:
            category = result.content_type or "other"
            summary["categories"][category] = summary["categories"].get(category, 0) + 1

        summary["avg_viral_score"] = sum(r.strategic_score for r in results) / len(results)

    return summary
