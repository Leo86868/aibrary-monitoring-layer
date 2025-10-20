"""
AIbrary TikTok Monitoring System - Base Processor
Abstract base class for all content processors
"""

from abc import ABC, abstractmethod
from typing import List
from core.models import MonitoringTarget, TikTokContent, ProcessingResult


class BaseProcessor(ABC):
    """Abstract base class for all target processors"""

    @abstractmethod
    def can_process(self, target: MonitoringTarget) -> bool:
        """Check if this processor can handle the given target"""
        pass

    @abstractmethod
    def process(self, target: MonitoringTarget) -> ProcessingResult:
        """Process the target and return results"""
        pass

    def _create_success_result(self, target: MonitoringTarget, content: List[TikTokContent], processing_time: float = None) -> ProcessingResult:
        """Helper to create successful processing result"""
        return ProcessingResult(
            target=target,
            success=True,
            content_found=content,
            processing_time=processing_time
        )

    def _create_error_result(self, target: MonitoringTarget, error_message: str, processing_time: float = None) -> ProcessingResult:
        """Helper to create error processing result"""
        return ProcessingResult(
            target=target,
            success=False,
            content_found=[],
            error_message=error_message,
            processing_time=processing_time
        )
