#!/usr/bin/env python3
"""
AIbrary TikTok Monitoring System - Core Module
Consolidated data models, configuration, and utilities
"""

import os
import time
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
from dotenv import load_dotenv

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Load .env from config directory
config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
env_path = os.path.join(config_dir, '.env')
load_dotenv(env_path)

# Lark API Configuration
LARK_APP_ID = os.getenv('LARK_APP_ID', 'cli_a860785f5078100d')
LARK_APP_SECRET = os.getenv('LARK_APP_SECRET', 'sfH5BBpCd6tTeqfPB1FRlhV3JQ6M723A')
LARK_BASE_ID = os.getenv('LARK_BASE_ID', 'Qr40bFHf8aKpBosZjXbcjF4rnXe')

# Apify Configuration
APIFY_TOKEN = os.getenv('APIFY_TOKEN')
TIKTOK_ACTOR_ID = os.getenv('TIKTOK_ACTOR_ID', 'GdWCkxBtKWOsKjdch')

# Table Names
MONITORING_TARGETS_TABLE = 'Monitoring_Targets'
TIKTOK_CONTENT_TABLE = 'TikTok_Content'

# Processing Configuration
DEFAULT_TIMEOUT = 600  # 10 minutes
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 1  # seconds between requests

# ==============================================================================
# DATA MODELS
# ==============================================================================

@dataclass
class MonitoringTarget:
    """Represents a target to monitor (profile, hashtag, search, etc.)"""
    record_id: str
    target_value: str
    platform: str
    target_type: str  # "profile", "hashtag", "search", "trend"
    active: bool
    results_limit: int
    team_notes: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

    @property
    def is_profile(self) -> bool:
        return self.target_type == "profile"

    @property
    def is_hashtag(self) -> bool:
        return self.target_type == "hashtag"

    @property
    def is_search(self) -> bool:
        return self.target_type == "search"

@dataclass
class TikTokContent:
    """Represents scraped TikTok content with media download support"""
    content_id: str
    target_value: str
    video_url: str
    author_username: str
    caption: str
    likes: int
    comments: int
    views: int
    engagement_rate: float
    team_status: str = "new"
    team_notes: Optional[str] = None
    discovered_date: Optional[datetime] = None
    # New fields for video downloads and AI analysis
    video_download_url: Optional[str] = ""
    subtitle_url: Optional[str] = ""
    ai_analysis_result: Optional[str] = ""
    video_analyzed: bool = False

    def __post_init__(self):
        if self.discovered_date is None:
            self.discovered_date = datetime.now()

    def calculate_engagement_rate(self) -> float:
        """Calculate engagement rate: (likes + comments) / views * 100"""
        if self.views == 0:
            return 0.0
        return ((self.likes + self.comments) / self.views) * 100

@dataclass
class ProcessingResult:
    """Result of processing a monitoring target"""
    target: MonitoringTarget
    success: bool
    content_found: List[TikTokContent]
    error_message: Optional[str] = None
    processing_time: Optional[float] = None