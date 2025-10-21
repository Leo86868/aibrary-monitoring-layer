#!/usr/bin/env python3
"""
AIbrary TikTok Monitoring System - Main Orchestrator
Complete TikTok monitoring pipeline in a single consolidated module
"""

import sys
import time
from typing import List
from datetime import datetime

from core import MonitoringTarget, ProcessingResult
from storage import LarkClient
from scraping import ProcessorFactory
from analysis import VideoAnalyzer, analyze_new_content

class TikTokMonitor:
    """Main orchestrator for TikTok monitoring system"""

    def __init__(self):
        self.lark_client = LarkClient()
        self.processor_factory = ProcessorFactory()
        self.ai_analyzer = VideoAnalyzer()

    def run(self) -> bool:
        """Run the complete monitoring pipeline"""
        start_time = time.time()
        print(f"🚀 Starting TikTok monitoring run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            # Step 1: Get active targets from Lark
            targets = self._get_active_targets()
            if not targets:
                print("⚠️ No active targets found")
                return True

            # Step 2: Filter to supported targets
            supported_targets, unsupported_targets = self._filter_targets(targets)

            if unsupported_targets:
                print(f"⚠️ Skipping {len(unsupported_targets)} unsupported targets:")
                for target in unsupported_targets:
                    print(f"   - {target.target_value} ({target.target_type})")

            if not supported_targets:
                print("❌ No supported targets found")
                return False

            # Step 3: Process each supported target (scrape only)
            results = self._process_targets(supported_targets)

            # Step 4: Save raw scraped content to Lark
            save_success = self._save_results(results)

            if not save_success:
                print("⚠️ Some content failed to save, but continuing to analysis...")

            # Step 5: Analyze content with strategy routing (read from Lark, analyze, update)
            analysis_success = self._analyze_and_update()

            # Step 6: Summary
            self._print_summary(results, time.time() - start_time)

            return save_success and analysis_success

        except Exception as e:
            print(f"❌ Processing failed: {e}")
            return False

    def _get_active_targets(self) -> List[MonitoringTarget]:
        """Get active monitoring targets from Lark"""
        print("📋 Loading active targets from Lark...")
        targets = self.lark_client.get_active_targets()
        print(f"   Found {len(targets)} active targets")
        return targets

    def _filter_targets(self, targets: List[MonitoringTarget]) -> tuple:
        """Filter targets into supported and unsupported"""
        print("🔍 Filtering targets by processor availability...")

        supported = self.processor_factory.get_supported_targets(targets)
        unsupported = self.processor_factory.get_unsupported_targets(targets)

        print(f"   ✅ Supported: {len(supported)}")
        print(f"   ⚠️ Unsupported: {len(unsupported)}")

        return supported, unsupported

    def _process_targets(self, targets: List[MonitoringTarget]) -> List[ProcessingResult]:
        """Process each target and collect results"""
        print(f"\\n⚡ Processing {len(targets)} targets...")

        results = []
        for i, target in enumerate(targets, 1):
            print(f"\\n[{i}/{len(targets)}] Processing: {target.target_value}")

            try:
                # Get appropriate processor
                processor = self.processor_factory.get_processor(target)
                if not processor:
                    print(f"❌ No processor available for {target.target_value}")
                    continue

                # Process target
                result = processor.process(target)
                results.append(result)

                # Brief delay between targets
                if i < len(targets):
                    time.sleep(1)

            except Exception as e:
                print(f"❌ Failed to process {target.target_value}: {e}")
                continue

        return results

    def _save_results(self, results: List[ProcessingResult]) -> bool:
        """Save raw scraped content to Lark (no analysis yet)"""
        print("\\n💾 Saving raw scraped content to Lark...")

        total_content = 0
        new_content_count = 0
        all_success = True

        for result in results:
            if result.success and result.content_found:
                total_content += len(result.content_found)

                # Filter out duplicates for this target
                new_content = []
                for content in result.content_found:
                    if not self.lark_client.content_exists(content.content_id):
                        new_content.append(content)

                new_content_count += len(new_content)

                # Save raw content with target linkage (NO analysis yet)
                if new_content:
                    print(f"   💾 Saving {len(new_content)} new items from {result.target.target_value}...")
                    success = self.lark_client.save_content(new_content, result.target.record_id)
                    if not success:
                        all_success = False

        print(f"   📊 Total content found: {total_content}")
        print(f"   🆕 New content saved: {new_content_count}")

        if new_content_count == 0:
            print("   ✅ All content already exists in database")
            return True

        return all_success

    def _analyze_and_update(self) -> bool:
        """
        Read content from Lark (with strategies populated by lookup),
        analyze based on strategy routing, and update with results
        """
        from core import TikTokContent, TIKTOK_CONTENT_TABLE

        print("\\n🔍 Reading content from Lark to analyze with strategy routing...")

        # Fetch all content from database
        table_id = self.lark_client._get_table_id(TIKTOK_CONTENT_TABLE)
        path = f"/bitable/v1/apps/{self.lark_client.base_id}/tables/{table_id}/records"

        try:
            data = self.lark_client._make_request("GET", path, {"page_size": 500})
        except Exception as e:
            print(f"❌ Failed to read content from Lark: {e}")
            return False

        if not data.get('items'):
            print("   ⚠️ No content in database to analyze")
            return True

        print(f"   Found {len(data['items'])} total records in database")

        # Filter to content that needs analysis (no strategic_score yet)
        to_analyze = []
        for item in data['items']:
            fields = item['fields']

            # Skip if already analyzed (has strategic_score)
            if fields.get('strategic_score'):
                continue

            # Decode monitoring_strategy from Lark lookup field
            # Strategy option ID to text mapping
            STRATEGY_MAPPING = {
                'optC7R9ojK': 'Competitor Intelligence',
                'optBbDImXA': 'Trend Discovery',
                'opt94KPGSJ': 'Niche Deep-Dive'
            }

            raw_strategy = fields.get('monitoring_strategy', None)
            strategy_text = None
            if raw_strategy and isinstance(raw_strategy, list) and len(raw_strategy) > 0:
                # Lark returns lookup as list - could be option ID or text
                option_value = raw_strategy[0].get("text") if isinstance(raw_strategy[0], dict) else raw_strategy[0]
                # Map option ID to text if needed
                strategy_text = STRATEGY_MAPPING.get(option_value, option_value)

            # Build TikTokContent object with strategy from Lark lookup
            content = TikTokContent(
                content_id=str(fields.get('content_id', '')),
                target_value=fields.get('target_value', '@unknown'),
                video_url=fields.get('video_url', {}).get('link', '') if isinstance(fields.get('video_url'), dict) else '',
                author_username=fields.get('author_username', ''),
                caption=fields.get('caption', ''),
                likes=int(fields.get('likes', 0)),
                comments=int(fields.get('comments', 0)),
                views=int(fields.get('views', 0)),
                engagement_rate=float(fields.get('engagement_rate', 0)),
                video_download_url=fields.get('video_downlaod_url', {}).get('link', '') if isinstance(fields.get('video_downlaod_url'), dict) else '',
                subtitle_url=fields.get('subtitle_url', {}).get('link', '') if isinstance(fields.get('subtitle_url'), dict) else '',
                monitoring_strategy=strategy_text  # ✅ Strategy from Lark lookup
            )

            # Store record_id for updating later
            content._record_id = item['record_id']
            to_analyze.append(content)

        if not to_analyze:
            print("   ✅ All content already analyzed!")
            return True

        print(f"   🎯 {len(to_analyze)} items need analysis\\n")

        # Run strategy-aware batch analysis
        print("🤖 Running AI analysis with strategy routing...")
        analysis_results = self.ai_analyzer.batch_analyze(to_analyze)

        if not analysis_results:
            print("   ⚠️ No analysis results (all content skipped or analysis disabled)")
            # Still return True - not an error, just nothing to analyze
            return True

        print(f"\\n   ✅ AI analysis completed for {len(analysis_results)} items")

        # Print full analysis results
        for analysis in analysis_results:
            print(f"\\n   📊 {analysis.content_id}: {analysis.content_type} | Strategic Score: {analysis.strategic_score}/10")
            print(f"   📝 Analysis: {analysis.general_analysis[:100]}...")
            print(f"   💡 Insights: {analysis.strategic_insights[:100]}...")

        # Update Lark with analysis results
        print("\\n💾 Updating Lark with analysis results...")

        update_success = True
        for content in to_analyze:
            # Only update if this content was analyzed (has strategic_score)
            if content.strategic_score is not None:
                record_id = getattr(content, '_record_id', None)
                if record_id:
                    success = self.lark_client.update_content(record_id, content)
                    if not success:
                        update_success = False

        return update_success

    def _print_summary(self, results: List[ProcessingResult], total_time: float):
        """Print processing summary"""
        print("\\n" + "="*50)
        print("📊 PROCESSING SUMMARY")
        print("="*50)

        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]
        total_content = sum(len(r.content_found) for r in successful)

        print(f"⏱️ Total time: {total_time:.1f}s")
        print(f"🎯 Targets processed: {len(results)}")
        print(f"✅ Successful: {len(successful)}")
        print(f"❌ Failed: {len(failed)}")
        print(f"📱 Content found: {total_content}")

        if successful:
            print("\\n✅ Successful targets:")
            for result in successful:
                print(f"   - {result.target.target_value}: {len(result.content_found)} videos ({result.processing_time:.1f}s)")

        if failed:
            print("\\n❌ Failed targets:")
            for result in failed:
                print(f"   - {result.target.target_value}: {result.error_message}")

        print("\\n🎉 Processing complete!")

def main():
    """Main entry point"""
    monitor = TikTokMonitor()
    success = monitor.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()