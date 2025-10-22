"""
AIbrary TikTok Monitoring System - Rule Matcher
Hierarchical rule matching for quality filtering
"""

from typing import List, Dict, Tuple, Optional
from core import FilterRule, TikTokContent, MonitoringTarget


def build_rule_index(rules: List[FilterRule]) -> Dict[Tuple[str, Optional[str], Optional[str]], FilterRule]:
    """
    Build hierarchical rule index from list of filter rules.

    Args:
        rules: List of FilterRule objects (active rules only)

    Returns:
        Dictionary mapping composite key tuples to FilterRule objects
        Key format: (monitoring_strategy, target_type, target_value)

    Example:
        {
            ("Competitor Intelligence", "profile", "@blinkist"): FilterRule(...),
            ("Competitor Intelligence", "profile", None): FilterRule(...),
            ("Niche Deep-Dive", "hashtag", None): FilterRule(...),
        }
    """
    index = {}

    for rule in rules:
        # Normalize empty strings to None for consistent matching
        target_type = rule.target_type if rule.target_type else None
        target_value = rule.target_value if rule.target_value else None

        # Create composite key
        key = (rule.monitoring_strategy, target_type, target_value)

        # Add to index (last rule wins if duplicate keys)
        index[key] = rule

    return index


def find_matching_rule(
    content: TikTokContent,
    target: MonitoringTarget,
    rule_index: Dict[Tuple[str, Optional[str], Optional[str]], FilterRule]
) -> Optional[FilterRule]:
    """
    Find the most specific filter rule matching content and target.

    Uses hierarchical matching (tries most specific first):
    1. (monitoring_strategy, target_type, target_value) - exact target match
    2. (monitoring_strategy, target_type, None)  - target type match
    3. (monitoring_strategy, None, None)  - strategy match

    Args:
        content: TikTokContent object to filter
        target: MonitoringTarget associated with this content
        rule_index: Pre-built rule index from build_rule_index()

    Returns:
        Most specific matching FilterRule, or None if no match
    """
    # Get strategy from target (required for matching)
    strategy = target.monitoring_strategy
    if not strategy:
        return None

    # Get target type and value
    target_type = target.target_type
    target_value = content.target_value

    # Try Level 3: Most specific (strategy + type + value)
    key = (strategy, target_type, target_value)
    if key in rule_index:
        return rule_index[key]

    # Try Level 2: Mid-specific (strategy + type)
    key = (strategy, target_type, None)
    if key in rule_index:
        return rule_index[key]

    # Try Level 1: Least specific (strategy only)
    key = (strategy, None, None)
    if key in rule_index:
        return rule_index[key]

    # No matching rule found
    return None
