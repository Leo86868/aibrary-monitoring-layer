"""
AIbrary TikTok Monitoring System - Core Module
Data models, configuration, and constants
"""

from .models import (
    MonitoringTarget,
    TikTokContent,
    ProcessingResult,
    AnalysisResult,
    FilterRule
)

from .config import (
    LARK_APP_ID,
    LARK_APP_SECRET,
    LARK_BASE_ID,
    APIFY_TOKEN,
    TIKTOK_ACTOR_ID,
    MONITORING_TARGETS_TABLE,
    TIKTOK_CONTENT_TABLE,
    DEFAULT_TIMEOUT,
    MAX_RETRIES,
    RATE_LIMIT_DELAY,
    GEMINI_API_KEY
)

__all__ = [
    # Models
    'MonitoringTarget',
    'TikTokContent',
    'ProcessingResult',
    'AnalysisResult',
    'FilterRule',
    # Config
    'LARK_APP_ID',
    'LARK_APP_SECRET',
    'LARK_BASE_ID',
    'APIFY_TOKEN',
    'TIKTOK_ACTOR_ID',
    'MONITORING_TARGETS_TABLE',
    'TIKTOK_CONTENT_TABLE',
    'DEFAULT_TIMEOUT',
    'MAX_RETRIES',
    'RATE_LIMIT_DELAY',
    'GEMINI_API_KEY'
]
