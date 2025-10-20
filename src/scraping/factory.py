"""
AIbrary TikTok Monitoring System - Processor Factory
Factory for creating appropriate processors for different target types
"""

from typing import List, Optional
from core import MonitoringTarget
from .base import BaseProcessor
from .profile_processor import ProfileProcessor
from .hashtag_processor import HashtagProcessor
from .search_processor import SearchProcessor


class ProcessorFactory:
    """Factory for creating appropriate processors for different target types"""

    def __init__(self):
        self.processors = [
            ProfileProcessor(),
            HashtagProcessor(),
            SearchProcessor()
        ]

    def get_processor(self, target: MonitoringTarget) -> Optional[BaseProcessor]:
        """Get the appropriate processor for a target"""
        for processor in self.processors:
            if processor.can_process(target):
                return processor
        return None

    def get_supported_targets(self, targets: List[MonitoringTarget]) -> List[MonitoringTarget]:
        """Filter targets to only those that have available processors"""
        return [target for target in targets if self.get_processor(target)]

    def get_unsupported_targets(self, targets: List[MonitoringTarget]) -> List[MonitoringTarget]:
        """Filter targets to only those that don't have available processors"""
        return [target for target in targets if not self.get_processor(target)]
