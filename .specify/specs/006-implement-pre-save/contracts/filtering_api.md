# API Contract: Filtering Module

**Feature**: 006-implement-pre-save
**Date**: 2025-10-21
**Module**: `src/filtering/`

## Overview

This document defines the public API contracts for the filtering module. These functions are called by `monitor.py` to filter scraped content before saving to Lark Base.

---

## Module: `src/filtering/rule_matcher.py`

### Function: `build_rule_index`

**Purpose**: Build hierarchical index from list of filter rules for efficient lookup

**Signature**:
```python
def build_rule_index(rules: List[FilterRule]) -> Dict[Tuple[str, Optional[str], Optional[str]], FilterRule]:
    """
    Build hierarchical rule index from list of filter rules.

    Args:
        rules: List of FilterRule objects (active rules only)

    Returns:
        Dictionary mapping composite key tuples to FilterRule objects
        Key format: (strategy, target_type, target_value)

    Example:
        {
            ("Competitor Intelligence", "profile", "@blinkist"): FilterRule(...),
            ("Competitor Intelligence", "profile", None): FilterRule(...),
            ("Niche Deep-Dive", "hashtag", None): FilterRule(...),
        }
    """
```

**Behavior**:
- Input: List of FilterRule objects
- Output: Dict with composite key tuples as keys
- Empty string target_type/target_value normalized to None
- Duplicate keys: Last rule wins (deterministic based on list order)
- Empty input list returns empty dict

**Error Handling**:
- No exceptions raised (handles empty list gracefully)
- Invalid rule types logged as warning and skipped

---

### Function: `find_matching_rule`

**Purpose**: Find the most specific filter rule matching the given content and target

**Signature**:
```python
def find_matching_rule(
    content: TikTokContent,
    target: MonitoringTarget,
    rule_index: Dict[Tuple[str, Optional[str], Optional[str]], FilterRule]
) -> Optional[FilterRule]:
    """
    Find most specific filter rule matching content and target.

    Args:
        content: TikTokContent object to filter
        target: MonitoringTarget associated with this content
        rule_index: Pre-built rule index from build_rule_index()

    Returns:
        Most specific matching FilterRule, or None if no match

    Matching order (specificity):
        1. (strategy, type, value) - exact target match
        2. (strategy, type, None)  - target type match
        3. (strategy, None, None)  - strategy match
    """
```

**Behavior**:
- Tries 3 lookups in order of specificity
- Returns first matching rule found
- Returns None if no match at any level
- Uses target.monitoring_strategy, target.target_type, content.target_value for matching

**Error Handling**:
- Returns None if target.monitoring_strategy is None (no filtering)
- Returns None if rule_index is empty (fail-open)

**Examples**:
```python
# Example 1: Exact target match
target = MonitoringTarget(monitoring_strategy="Competitor Intelligence", target_type="profile", ...)
content = TikTokContent(target_value="@blinkist", ...)
rule_index = {
    ("Competitor Intelligence", "profile", "@blinkist"): rule1,  # Will match this
    ("Competitor Intelligence", "profile", None): rule2,
}
result = find_matching_rule(content, target, rule_index)
# Returns: rule1 (level 3 match)

# Example 2: Type match (no exact target)
target = MonitoringTarget(monitoring_strategy="Niche Deep-Dive", target_type="hashtag", ...)
content = TikTokContent(target_value="#books", ...)
rule_index = {
    ("Niche Deep-Dive", "hashtag", None): rule3,  # Will match this
    ("Niche Deep-Dive", None, None): rule4,
}
result = find_matching_rule(content, target, rule_index)
# Returns: rule3 (level 2 match)

# Example 3: No match
target = MonitoringTarget(monitoring_strategy="Unknown Strategy", ...)
result = find_matching_rule(content, target, rule_index)
# Returns: None (no filtering)
```

---

## Module: `src/filtering/content_filter.py`

### Function: `passes_filter`

**Purpose**: Check if content passes the thresholds defined in a filter rule (OR logic)

**Signature**:
```python
def passes_filter(content: TikTokContent, rule: FilterRule) -> bool:
    """
    Check if content passes filter rule thresholds using OR logic.

    Args:
        content: TikTokContent object to evaluate
        rule: FilterRule with threshold values

    Returns:
        True if content passes (meets ANY threshold), False otherwise

    Logic:
        - Returns True if ANY threshold is met (OR logic)
        - Returns True if all thresholds are None (pass-through rule)
        - Returns True if all thresholds fail but at least one is set (fail-open)
    """
```

**Behavior**:
- Evaluates each threshold independently
- Short-circuit: Returns True on first threshold met
- Missing content metrics (None) treated as 0
- Engagement rate calculated if not provided: `(likes / views * 100) if views > 0 else 0`
- Age calculated if max_age_days is set: `(datetime.now() - created_at).days`

**Threshold Evaluation**:
```python
# Likes check
if rule.min_likes is not None and content.likes >= rule.min_likes:
    return True

# Views check
if rule.min_views is not None and content.views >= rule.min_views:
    return True

# Engagement rate check
if rule.min_engagement_rate is not None:
    engagement = calculate_engagement_rate(content)
    if engagement >= rule.min_engagement_rate:
        return True

# Age check
if rule.max_age_days is not None:
    age = calculate_age_days(content)
    if age <= rule.max_age_days:
        return True

# No thresholds met, but fail-open (prefer false positives)
return True
```

**Error Handling**:
- No exceptions raised
- Missing created_at for age check: Assumes content is recent (passes age check)
- Division by zero in engagement calculation: Returns 0 engagement

**Examples**:
```python
# Example 1: Passes likes threshold
content = TikTokContent(likes=6000, views=10000, ...)
rule = FilterRule(min_likes=5000, min_views=20000, ...)
result = passes_filter(content, rule)
# Returns: True (6000 >= 5000, even though views=10000 < 20000)

# Example 2: Fails all thresholds
content = TikTokContent(likes=100, views=500, ...)
rule = FilterRule(min_likes=5000, min_views=10000, min_engagement_rate=5.0, ...)
result = passes_filter(content, rule)
# Returns: True (fail-open - prefer to save than to lose data)

# Example 3: Passes engagement rate
content = TikTokContent(likes=300, views=1000, ...)
rule = FilterRule(min_engagement_rate=20.0, ...)
result = passes_filter(content, rule)
# Returns: True (300/1000*100 = 30% >= 20%)
```

---

### Function: `filter_content_list`

**Purpose**: Filter a list of content items, returning only those that pass filtering

**Signature**:
```python
def filter_content_list(
    content_list: List[TikTokContent],
    target: MonitoringTarget,
    rule_index: Dict[Tuple[str, Optional[str], Optional[str]], FilterRule]
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
```

**FilterMetrics Structure**:
```python
@dataclass
class FilterMetrics:
    total_scraped: int      # Total items in input list
    filtered_out: int       # Items that failed filter
    saved: int              # Items that passed filter (total_scraped - filtered_out)
    rule_used: Optional[FilterRule]  # Rule applied, or None if no filtering
```

**Behavior**:
1. Find matching rule using `find_matching_rule()`
2. If no rule found: Return all content (fail-open)
3. For each content item: Evaluate using `passes_filter()`
4. Build filtered list containing only passing items
5. Calculate and return metrics

**Error Handling**:
- Empty content_list: Returns ([], FilterMetrics(0, 0, 0, None))
- No matching rule: Returns (content_list, FilterMetrics(len(content_list), 0, len(content_list), None))
- Exception during filtering: Log warning, include item (fail-open per-item)

**Examples**:
```python
# Example 1: Normal filtering
content_list = [content1, content2, content3]  # 3 items
rule_index = {...}  # Has matching rule with min_likes=5000
result, metrics = filter_content_list(content_list, target, rule_index)
# Returns: ([content1, content3], FilterMetrics(3, 1, 2, rule))
# Interpretation: 3 scraped, 1 filtered out, 2 saved

# Example 2: No matching rule (fail-open)
content_list = [content1, content2, content3]
rule_index = {}  # Empty
result, metrics = filter_content_list(content_list, target, rule_index)
# Returns: ([content1, content2, content3], FilterMetrics(3, 0, 3, None))
# Interpretation: All content saved (no filtering applied)
```

---

## Module: `src/storage/lark_client.py` (Additions)

### Function: `get_filter_rules`

**Purpose**: Fetch active filter rules from Lark Base Filter_Rules table

**Signature**:
```python
def get_filter_rules(self) -> List[FilterRule]:
    """
    Fetch active filter rules from Lark Base.

    Returns:
        List of FilterRule objects with active=True
        Empty list if table doesn't exist or API error (fail-open)
    """
```

**Behavior**:
1. Get table ID for "Filter_Rules" table
2. Fetch all records (paginate if >500 records)
3. Parse each record into FilterRule object
4. Filter to only active rules (active=True)
5. Return list

**Field Mapping** (Lark ’ Python):
```python
{
    "strategy": str(fields.get("strategy", "")),
    "target_type": str(fields.get("target_type", "")) or None,
    "target_value": str(fields.get("target_value", "")) or None,
    "min_likes": int(fields.get("min_likes")) if fields.get("min_likes") else None,
    "min_views": int(fields.get("min_views")) if fields.get("min_views") else None,
    "min_engagement_rate": float(fields.get("min_engagement_rate")) if fields.get("min_engagement_rate") else None,
    "max_age_days": int(fields.get("max_age_days")) if fields.get("max_age_days") else None,
    "active": bool(fields.get("active", True)),
}
```

**Error Handling**:
- Table not found: Return empty list (fail-open)
- API error: Log warning, return empty list (fail-open)
- Invalid record format: Skip record, log warning, continue
- No active rules: Return empty list (no filtering)

---

## Integration Example

**Usage in `monitor.py`**:
```python
from filtering.rule_matcher import build_rule_index, find_matching_rule
from filtering.content_filter import filter_content_list

# Phase 1: Load filter rules once at pipeline start
lark = LarkClient()
filter_rules = lark.get_filter_rules()
rule_index = build_rule_index(filter_rules)

# Phase 2: For each target, scrape and filter
for target in targets:
    # Scrape content
    processor = get_processor(target)
    result = processor.process(target)
    content_list = result.content_list

    # Filter before saving
    filtered_content, metrics = filter_content_list(content_list, target, rule_index)

    # Report metrics
    print(f"   {metrics.total_scraped} scraped ’ {metrics.saved} saved ({metrics.filtered_out} filtered out)")

    # Save only filtered content
    lark.save_content(filtered_content)
```

---

## Error Handling Summary

| Scenario | Behavior | Rationale |
|----------|----------|-----------|
| No matching rule | Save all content (fail-open) | Prefer data over cleanliness |
| Rule loading fails | Save all content (fail-open) | API outage shouldn't block pipeline |
| Content passes no thresholds | Save anyway (fail-open) | Avoid accidental data loss |
| Invalid content data | Skip item, log warning | Protect pipeline from bad data |
| Empty content list | Return empty list, metrics=(0,0,0,None) | No-op case |

---

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|------------|-------|
| `build_rule_index()` | O(n) | n = number of rules (10-50) |
| `find_matching_rule()` | O(1) | 3 dict lookups maximum |
| `passes_filter()` | O(1) | 4 threshold checks maximum |
| `filter_content_list()` | O(m) | m = number of content items (100-200) |
| **Total per pipeline run** | O(n + m*targets) | Typically <1 second for 10 targets, 100 items each |

**Performance Goals**: <5 seconds for 100 items per target (met with O(1) rule matching)
