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
from data import LarkClient
from processing import ProcessorFactory

class TikTokMonitor:
    """Main orchestrator for TikTok monitoring system"""

    def __init__(self):
        self.lark_client = LarkClient()
        self.processor_factory = ProcessorFactory()

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

            # Step 3: Process each supported target
            results = self._process_targets(supported_targets)

            # Step 4: Save results to Lark
            success = self._save_results(results)

            # Step 5: Summary
            self._print_summary(results, time.time() - start_time)

            return success

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
        """Save processing results to Lark with target linkage"""
        print("\\n💾 Saving results to Lark...")

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

                # Save content with target linkage
                if new_content:
                    success = self.lark_client.save_content(new_content, result.target.record_id)
                    if not success:
                        all_success = False

        print(f"   📊 Total content found: {total_content}")
        print(f"   🆕 New content: {new_content_count}")

        if new_content_count == 0:
            print("   ✅ All content already exists")
            return True

        return all_success

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