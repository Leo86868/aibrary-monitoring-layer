#!/usr/bin/env python3
"""
Debug Apify output to see what data we're actually getting
"""

import sys
import os
import json

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import APIFY_TOKEN, TIKTOK_ACTOR_ID, DEFAULT_TIMEOUT
import requests

def debug_apify_response():
    """Debug what Apify actually returns"""

    if not APIFY_TOKEN:
        print("❌ APIFY_TOKEN not found")
        return

    token = APIFY_TOKEN.strip()

    # Same input as our processor
    run_input = {
        "profiles": ["@openai"],
        "resultsPerPage": 3,  # Just get 3 for debugging
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
        "shouldDownloadSubtitles": False,
        "proxyConfiguration": {"useApifyProxy": True}
    }

    print("🚀 Debugging Apify response...")
    print(f"📊 Actor: {TIKTOK_ACTOR_ID}")
    print(f"📋 Input: {json.dumps(run_input, indent=2)}")

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

        print(f"\n📊 Response type: {type(dataset_items)}")
        print(f"📊 Number of items: {len(dataset_items) if isinstance(dataset_items, list) else 'N/A'}")

        if dataset_items:
            print("\n🔍 First item raw data:")
            first_item = dataset_items[0] if isinstance(dataset_items, list) else dataset_items
            print(json.dumps(first_item, indent=2))

            print("\n🔍 Available fields in first item:")
            if isinstance(first_item, dict):
                for key, value in first_item.items():
                    print(f"   {key}: {type(value).__name__} = {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")

        print("\n✅ Debug complete!")

    except Exception as e:
        print(f"❌ Debug failed: {e}")

if __name__ == "__main__":
    debug_apify_response()