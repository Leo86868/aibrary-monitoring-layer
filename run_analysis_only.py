#!/usr/bin/env python3
"""
Run AI Analysis Only - Re-analyze existing content in database

This script re-runs Phase 5 (AI Analysis) on all content that doesn't have analysis yet.
Useful when you've cleared the AI columns and want to re-analyze with updated prompts.
"""

import sys
sys.path.insert(0, 'src')

from storage import LarkClient
from analysis import VideoAnalyzer
from core import TikTokContent, TIKTOK_CONTENT_TABLE

def main():
    print("=" * 70)
    print("🤖 AI ANALYSIS ONLY - Re-analyzing existing content")
    print("=" * 70)

    # Initialize
    lark = LarkClient()
    analyzer = VideoAnalyzer()

    # Fetch all content from database
    print("\n📋 Fetching content from database...")
    table_id = lark._get_table_id(TIKTOK_CONTENT_TABLE)
    path = f"/bitable/v1/apps/{lark.base_id}/tables/{table_id}/records?page_size=500"
    data = lark._make_request("GET", path)

    if not data.get('items'):
        print("❌ No content in database")
        return

    total = len(data['items'])
    print(f"   Found {total} total records")

    # Strategy mapping for decoding
    STRATEGY_MAP = {
        "optC7R9ojK": "Competitor Intelligence",
        "optBbDImXA": "Trend Discovery",
        "opt94KPGSJ": "Niche Deep-Dive"
    }

    # Filter to content that needs analysis (missing Analysis field)
    to_analyze = []
    for item in data['items']:
        fields = item['fields']

        # Check if already analyzed
        if fields.get('Analysis'):
            continue

        # Decode monitoring_strategy from lookup field
        raw_strategy = fields.get('monitoring_strategy', None)
        strategy_text = None
        if raw_strategy and isinstance(raw_strategy, list) and len(raw_strategy) > 0:
            # Lark returns lookup as list with option IDs
            strategy_id = raw_strategy[0]
            strategy_text = STRATEGY_MAP.get(strategy_id, None)

        # Build TikTokContent object
        content = TikTokContent(
            content_id=str(fields.get('content_id', '')),
            target_value=fields.get('target_value', '@unknown'),
            video_url=fields.get('video_url', {}).get('link', ''),
            author_username=fields.get('author_username', ''),
            caption=fields.get('caption', ''),
            likes=int(fields.get('likes', 0)),
            comments=int(fields.get('comments', 0)),
            views=int(fields.get('views', 0)),
            engagement_rate=float(fields.get('engagement_rate', 0)),
            video_download_url=fields.get('video_downlaod_url', {}).get('link', ''),  # Note: typo in field name
            subtitle_url=fields.get('subtitle_url', {}).get('link', ''),
            monitoring_strategy=strategy_text  # Add monitoring strategy
        )
        to_analyze.append(content)

    if not to_analyze:
        print("✅ All content already analyzed!")
        return

    print(f"🎯 {len(to_analyze)} items need analysis\n")

    # Run batch analysis
    print("🤖 Running AI analysis with new prompt...")
    print("   (This may take 60-90 seconds per video with video analysis enabled)\n")

    results = analyzer.batch_analyze(to_analyze, "competitor_intelligence")

    if not results:
        print("❌ Analysis failed")
        return

    print(f"\n✅ Analysis completed for {len(results)} items!")

    # Save updated content back to Lark Base
    print("\n💾 Saving analysis results to Lark Base...")

    # The batch_analyze method already updated the to_analyze content objects with analysis results
    # Now we just need to save them using save_content which will update existing records
    if lark.save_content(to_analyze):
        print(f"   ✅ Saved {len(to_analyze)} updated records to database")
    else:
        print("   ⚠️ Some records may not have saved properly")

    # Show sample results
    print("\n" + "=" * 70)
    print("📊 SAMPLE RESULTS (first 3)")
    print("=" * 70)

    for i, analysis in enumerate(results[:3], 1):
        print(f"\n[{i}] {analysis.content_id}")
        print(f"   Score: {analysis.strategic_score}/10")
        print(f"   Type: {analysis.content_type}")
        print(f"   Analysis: {analysis.general_analysis[:150]}...")
        print(f"   Insights: {analysis.strategic_insights[:150]}...")

    print("\n" + "=" * 70)
    print("✅ COMPLETE! Check your Lark Base to see all updated records")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
