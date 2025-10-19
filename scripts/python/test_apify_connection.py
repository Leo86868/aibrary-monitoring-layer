#!/usr/bin/env python3
"""
Test Apify connection and token
"""

import os
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load environment variables
load_dotenv()

def test_apify_connection():
    """Test if Apify token is valid"""

    # Get token from environment
    token = os.getenv('APIFY_TOKEN')

    if not token:
        print("❌ APIFY_TOKEN not found in environment")
        return False

    if token == "YOUR_APIFY_TOKEN_HERE":
        print("❌ APIFY_TOKEN not set (still has placeholder value)")
        return False

    print(f"✅ APIFY_TOKEN found: {token[:10]}...")

    try:
        # Initialize client
        client = ApifyClient(token)

        # Test by getting user info
        user = client.user().get()
        print(f"✅ Connected to Apify as: {user.get('username', 'Unknown')}")

        # List available actors (first 5)
        print("\\n📋 Available actors:")
        actors = client.actors().list(limit=5)
        for actor in actors.get('items', []):
            print(f"   - {actor['id']}: {actor['name']}")

        return True

    except Exception as e:
        print(f"❌ Apify connection failed: {e}")
        return False

if __name__ == "__main__":
    test_apify_connection()