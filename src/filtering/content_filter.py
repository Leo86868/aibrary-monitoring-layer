"""
AIbrary TikTok Monitoring System - Content Filter
Apply filter rules to content and track metrics
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from datetime import datetime
from core import TikTokContent, FilterRule, MonitoringTarget
from .rule_matcher import find_matching_rule


@dataclass
class FilterMetrics:
    """
    Metrics for content filtering operation.

    Attributes:
        total_scraped: Total items in input list
        filtered_out: Items that failed filter
        saved: Items that passed filter (total_scraped - filtered_out)
        rule_used: Rule applied, or None if no filtering
    """
    total_scraped: int
    filtered_out: int
    saved: int
    rule_used: Optional[FilterRule]


def passes_filter(content: TikTokContent, rule: FilterRule) -> bool:
    """
    Check if content passes filter rule thresholds using OR logic.

    Content passes if ANY threshold is met (not all).

    Args:
        content: TikTokContent object to evaluate
        rule: FilterRule with threshold values

    Returns:
        True if content passes (meets ANY threshold), False otherwise
    """
    # If no thresholds are set, pass by default (fail-open)
    has_any_threshold = (
        rule.min_likes is not None or
        rule.min_views is not None or
        rule.min_engagement_rate is not None or
        rule.max_age_days is not None
    )

    if not has_any_threshold:
        return True

    # Check likes threshold
    if rule.min_likes is not None:
        if content.likes >= rule.min_likes:
            return True

    # Check views threshold
    if rule.min_views is not None:
        if content.views >= rule.min_views:
            return True

    # Check engagement rate threshold
    if rule.min_engagement_rate is not None:
        # Calculate engagement rate if not provided
        if content.engagement_rate is None or content.engagement_rate == 0:
            if content.views > 0:
                content.engagement_rate = (content.likes / content.views) * 100
            else:
                content.engagement_rate = 0

        if content.engagement_rate >= rule.min_engagement_rate:
            return True

    # Check age threshold (if content has timestamp)
    if rule.max_age_days is not None and content.discovered_date:
        age_days = (datetime.now() - content.discovered_date).days
        if age_days <= rule.max_age_days:
            return True

    # No thresholds met - filter out low-quality content
    return False


def filter_content_list(
    content_list: List[TikTokContent],
    target: MonitoringTarget,
    rule_index: Dict
) -> Tuple[List[TikTokContent], FilterMetrics]:
    """
    Filter content list based on matching rule for target.

    Args:
        content_list: List of TikTokContent objects to filter
        target: MonitoringTarget associated with this content
        rule_index: Pre-built rule index from build_rule_index()

    Returns:
        Tuple of (filtered_content_list, metrics)
        filtered_content_list: List containing only content that passed filter
        metrics: FilterMetrics object with counts
    """
    total_scraped = len(content_list)

    # If no content, return empty list
    if total_scraped == 0:
        return [], FilterMetrics(0, 0, 0, None)

    # Find matching rule for this target
    # Use first content item to get target_value for matching
    rule = find_matching_rule(content_list[0], target, rule_index)

    # If no matching rule, pass all content (fail-open)
    if rule is None:
        return content_list, FilterMetrics(total_scraped, 0, total_scraped, None)

    # Filter content based on rule
    filtered_content = []
    for content in content_list:
        if passes_filter(content, rule):
            filtered_content.append(content)

    filtered_out = total_scraped - len(filtered_content)
    saved = len(filtered_content)

    metrics = FilterMetrics(
        total_scraped=total_scraped,
        filtered_out=filtered_out,
        saved=saved,
        rule_used=rule
    )

    return filtered_content, metrics
