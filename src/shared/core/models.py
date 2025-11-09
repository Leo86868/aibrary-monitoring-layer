"""
AIbrary TikTok Monitoring System - Data Models
Core data structures for the monitoring system
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime

# ==============================================================================
# MONITORING MODELS
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
    monitoring_strategy: Optional[str] = None  # "Competitor Intelligence", "Trend Discovery", "Niche Deep-Dive"
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

    # Strategic AI Analysis Fields (simplified for competitor intelligence)
    strategic_score: Optional[int] = None  # 0-10: Combined relevance + quality score for competitive value
    content_type: Optional[str] = None  # Controlled list: book_content, learning_feature, educational_value, etc.
    strategic_insights: Optional[str] = None  # Numbered insights (1-3 points) on competitive intelligence

    # Monitoring Strategy Classification (lookup field from Target table)
    # Auto-populated via Lark Base lookup from Monitoring Targets table
    # Values: "Competitor Intelligence", "Trend Discovery", "Niche Deep-Dive"
    # Used for routing to strategy-specific AI analysis prompts
    monitoring_strategy: Optional[str] = None

    # Niche Category (Niche Deep-Dive strategy only)
    # AI-assigned category for Niche Deep-Dive content
    # Values: "Podcasts & Audio Learning", "Books & Reading", "Productivity & Habits",
    #         "AI in Education", "Upskilling & Career", "Knowledge Management", "Other"
    # Used for grid view segmentation and filtering
    niche_category: Optional[str] = None

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

@dataclass(frozen=True)
class FilterRule:
    """
    Represents a quality filtering rule with hierarchical matching.

    Hierarchical matching levels:
    - Level 3 (most specific): monitoring_strategy + target_type + target_value
    - Level 2 (mid-specific): monitoring_strategy + target_type + None
    - Level 1 (least specific): monitoring_strategy + None + None

    Content passes filter if ANY threshold is met (OR logic).
    """
    monitoring_strategy: str  # Required: "Competitor Intelligence", "Trend Discovery", "Niche Deep-Dive"
    target_type: Optional[str] = None  # Optional: "profile", "hashtag", "search" - None = wildcard
    target_value: Optional[str] = None  # Optional: "@blinkist", "#book" - None = wildcard
    min_likes: Optional[int] = None  # Minimum likes threshold
    min_views: Optional[int] = None  # Minimum views threshold
    min_engagement_rate: Optional[float] = None  # Minimum engagement rate % (e.g., 2.5 for 2.5%)
    max_age_days: Optional[int] = None  # Maximum content age in days
    active: bool = True  # Whether this rule is enabled

# ==============================================================================
# AI ANALYSIS MODELS
# ==============================================================================

@dataclass
class AnalysisResult:
    """Result of AI analysis on TikTok content"""
    content_id: str
    summary: str  # General content description (Stage 1)
    general_analysis: Optional[str] = None  # Detailed Stage 1 analysis
    strategic_score: Optional[int] = None  # 0-10 combined score
    content_type: Optional[str] = None  # Controlled category
    strategic_insights: Optional[str] = None  # Numbered insights
    error: Optional[str] = None
