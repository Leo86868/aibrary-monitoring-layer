#!/usr/bin/env python3
"""
Test what video/subtitle URLs we're extracting
"""

import sys
import os
import json

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import APIFY_TOKEN, TIKTOK_ACTOR_ID, DEFAULT_TIMEOUT, MonitoringTarget
from processing import ProfileProcessor
import requests

def test_extraction():
    """Test video/subtitle URL extraction without saving"""

    # Create a test target
    target = MonitoringTarget(
        record_id="test123",
        target_value="@openai",
        platform="tiktok",
        target_type="profile",
        active=True,
        results_limit=2
    )

    # Create processor
    processor = ProfileProcessor()

    # Get raw data from Apify
    token = APIFY_TOKEN.strip()
    run_input = {
        "profiles": ["@openai"],
        "resultsPerPage": 2,
        "shouldDownloadVideos": True,
        "shouldDownloadCovers": False,
        "shouldDownloadSubtitles": True,
        "proxyConfiguration": {"useApifyProxy": True}
    }

    print("🚀 Testing video/subtitle extraction...")

    try:
        url = f"https://api.apify.com/v2/acts/{TIKTOK_ACTOR_ID}/run-sync-get-dataset-items"
        response = requests.post(
            url,
            params={"token": token},
            json=run_input,
            timeout=DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        dataset_items = response.json()

        # Process through our extraction logic
        content_list = processor._process_dataset_items(dataset_items, target)

        print(f"\n📊 Extracted {len(content_list)} content items:")

        for content in content_list:
            print(f"\n🎬 Content ID: {content.content_id}")
            print(f"   📝 Caption: {content.caption[:100]}...")
            print(f"   🎥 Video URL: {content.video_download_url[:100]}...")
            print(f"   📄 Subtitle URL: {content.subtitle_url[:100]}...")
            print(f"   🔗 Has video: {'✅' if content.video_download_url else '❌'}")
            print(f"   🔗 Has subtitle: {'✅' if content.subtitle_url else '❌'}")

        print(f"\n✅ Extraction test complete!")

    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_extraction()