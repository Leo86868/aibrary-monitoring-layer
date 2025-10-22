# Data Model: Pre-Save Quality Filtering System

**Feature**: 006-implement-pre-save
**Date**: 2025-10-21
**Phase**: 1 - Design & Contracts

## Overview

This document defines the data structures used in the quality filtering system. The core entity is `FilterRule`, which represents a single filtering rule with hierarchical matching keys and threshold values.

---

## Entity: FilterRule

**Purpose**: Represents a quality filtering rule with composite key for hierarchical matching and threshold values for content evaluation.

**Location**: `src/core/models.py` (add to existing models file)

### Fields

| Field Name | Type | Required | Default | Description |
|------------|------|----------|---------|-------------|
| `strategy` | `str` | Yes | - | Monitoring strategy ("Competitor Intelligence", "Trend Discovery", "Niche Deep-Dive") |
| `target_type` | `Optional[str]` | No | `None` | Target type ("profile", "hashtag", "search"). None = wildcard (strategy-level rule) |
| `target_value` | `Optional[str]` | No | `None` | Specific target ("@blinkist", "#book"). None = wildcard (type-level or strategy-level rule) |
| `min_likes` | `Optional[int]` | No | `None` | Minimum likes threshold. None = no likes requirement |
| `min_views` | `Optional[int]` | No | `None` | Minimum views threshold. None = no views requirement |
| `min_engagement_rate` | `Optional[float]` | No | `None` | Minimum engagement rate (%) threshold. None = no engagement requirement |
| `max_age_days` | `Optional[int]` | No | `None` | Maximum content age in days. None = no age requirement |
| `active` | `bool` | Yes | `True` | Whether this rule is active. Inactive rules are ignored |

### Validation Rules

1. **Strategy validation**: `strategy` must be non-empty string
2. **Threshold validation**: All threshold fields (min_likes, min_views, etc.) must be >= 0 if provided
3. **Specificity consistency**: If `target_value` is set, `target_type` must also be set (can't have target-specific rule without type)
4. **Wildcard representation**: Empty string ("") and None both treated as wildcard for `target_type` and `target_value`

### Hierarchical Matching Key

**Composite Key**: `(strategy, target_type, target_value)`

**Specificity Levels**:
1. **Level 3 (Most Specific)**: `(strategy, target_type, target_value)` - e.g., ("Competitor Intelligence", "profile", "@blinkist")
2. **Level 2 (Mid-Specific)**: `(strategy, target_type, None)` - e.g., ("Competitor Intelligence", "profile", None)
3. **Level 1 (Least Specific)**: `(strategy, None, None)` - e.g., ("Competitor Intelligence", None, None)

**Matching Logic**:
- Try level 3 first (exact target match)
- Fall back to level 2 (target type match)
- Fall back to level 1 (strategy match)
- If no match found, return None (no filtering, fail-open)

### State Transitions

**Rule Lifecycle**:
```
Created (active=True) ’ Active ’ Inactive (active=False) ’ [Can be reactivated]
                         “
                    Applied to content filtering
```

**State Changes**:
- **Created**: Rule added to Lark Base Filter_Rules table
- **Active**: Rule with `active=True` is loaded during pipeline run
- **Inactive**: Rule with `active=False` is ignored during rule loading
- **Reactivated**: User can set `active=True` again to re-enable rule

### Example Instances

**Example 1: Target-Specific Rule (Level 3)**
```python
FilterRule(
    strategy="Competitor Intelligence",
    target_type="profile",
    target_value="@blinkist",
    min_likes=1000,
    min_views=5000,
    min_engagement_rate=None,
    max_age_days=None,
    active=True
)
```
**Interpretation**: For @blinkist profile content under Competitor Intelligence, require at least 1000 likes OR 5000 views.

**Example 2: Type-Specific Rule (Level 2)**
```python
FilterRule(
    strategy="Niche Deep-Dive",
    target_type="hashtag",
    target_value=None,  # Wildcard
    min_likes=10000,
    min_views=50000,
    min_engagement_rate=2.0,
    max_age_days=30,
    active=True
)
```
**Interpretation**: For all hashtag targets under Niche Deep-Dive, require at least 10K likes OR 50K views OR 2% engagement rate, and content must be <30 days old.

**Example 3: Strategy-Level Rule (Level 1)**
```python
FilterRule(
    strategy="Trend Discovery",
    target_type=None,  # Wildcard
    target_value=None,  # Wildcard
    min_likes=20000,
    min_views=100000,
    min_engagement_rate=5.0,
    max_age_days=7,
    active=True
)
```
**Interpretation**: For all Trend Discovery content (any type, any target), require at least 20K likes OR 100K views OR 5% engagement rate, and content must be <7 days old (recent viral content only).

---

## Entity: TikTokContent (Existing, Updated)

**Purpose**: Represents scraped TikTok content. Used in filtering to compare engagement metrics against FilterRule thresholds.

**Location**: `src/core/models.py` (already exists)

### Fields Used in Filtering

| Field Name | Type | Usage in Filtering |
|------------|------|-------------------|
| `likes` | `int` | Compared against `FilterRule.min_likes` |
| `views` | `int` | Compared against `FilterRule.min_views` |
| `engagement_rate` | `float` | Compared against `FilterRule.min_engagement_rate` |
| `created_at` | `Optional[datetime]` | Used to calculate age for `FilterRule.max_age_days` check |
| `target_value` | `str` | Used to match against `FilterRule.target_value` for target-specific rules |

### Calculated Fields

**engagement_rate** (if not provided by scraper):
- Formula: `(likes / views) * 100`
- Calculated during filtering if `engagement_rate` is None
- Safe division: Returns 0 if `views == 0`

**age_in_days** (calculated on demand):
- Formula: `(datetime.now() - created_at).days`
- Only calculated if `FilterRule.max_age_days` is not None
- Returns infinity if `created_at` is None (always passes age check)

---

## Entity: MonitoringTarget (Existing, No Changes)

**Purpose**: Represents a monitoring target. Used to match content to appropriate filter rules.

**Location**: `src/core/models.py` (already exists)

### Fields Used in Filtering

| Field Name | Type | Usage in Filtering |
|------------|------|-------------------|
| `monitoring_strategy` | `Optional[str]` | Used to match `FilterRule.strategy` |
| `target_type` | `str` | Used to match `FilterRule.target_type` |
| `target_value` | `str` | Used to match `FilterRule.target_value` |

---

## Data Flow

### Loading Filter Rules from Lark Base

```
Lark Base Filter_Rules Table
    “
LarkClient.get_filter_rules()
    “
List[FilterRule] (in-memory cache)
    “
RuleMatcher.build_rule_index()
    “
Dict[(strategy, type, value), FilterRule] (lookup index)
```

### Applying Filters to Content

```
TikTokContent item
    “
RuleMatcher.find_matching_rule(item, target)
    “
FilterRule (or None if no match)
    “
ContentFilter.passes_filter(item, rule)
    “
Boolean (True = save, False = filter out)
```

---

## Relationships

### FilterRule ” MonitoringTarget

**Relationship**: Many-to-Many (implicit)
- One FilterRule can apply to multiple MonitoringTargets (e.g., strategy-level rule applies to all targets)
- One MonitoringTarget can match multiple FilterRules (but only most specific is used)

**Matching Logic**:
```python
def matches(rule: FilterRule, target: MonitoringTarget) -> bool:
    """Check if rule applies to target"""
    if rule.strategy != target.monitoring_strategy:
        return False
    if rule.target_type and rule.target_type != target.target_type:
        return False
    if rule.target_value and rule.target_value != target.target_value:
        return False
    return True
```

### FilterRule ” TikTokContent

**Relationship**: Many-to-Many (implicit)
- One FilterRule evaluates many TikTokContent items
- One TikTokContent item is evaluated against one matching FilterRule (or none)

**Evaluation Logic**:
```python
def passes_filter(content: TikTokContent, rule: FilterRule) -> bool:
    """Check if content passes rule thresholds (OR logic)"""
    if rule.min_likes and content.likes >= rule.min_likes:
        return True
    if rule.min_views and content.views >= rule.min_views:
        return True
    if rule.min_engagement_rate and content.engagement_rate >= rule.min_engagement_rate:
        return True
    # If all thresholds are None or all fail, pass by default (fail-open)
    return True
```

---

## Indexing Strategy

### Rule Index Structure

**Primary Index**: Dictionary with composite key tuple
```python
{
    ("Competitor Intelligence", "profile", "@blinkist"): FilterRule(...),
    ("Competitor Intelligence", "profile", None): FilterRule(...),
    ("Competitor Intelligence", None, None): FilterRule(...),
    ("Niche Deep-Dive", "hashtag", None): FilterRule(...),
}
```

**Lookup Performance**: O(1) average case per specificity level
- 3 lookups maximum per content item (level 3 ’ level 2 ’ level 1)
- No iteration through rule list needed

### Optimization Notes

- Build index once during rule loading (not per content item)
- Index is read-only during filtering (immutable frozen dataclasses)
- No need for thread-safety (single-threaded pipeline)

---

## Data Persistence

### Lark Base Schema

**Table Name**: `Filter_Rules`

**Columns** (Lark Base field names):
- `strategy` (Select: Competitor Intelligence, Trend Discovery, Niche Deep-Dive)
- `target_type` (Select: profile, hashtag, search)
- `target_value` (Text, optional)
- `min_likes` (Number, optional)
- `min_views` (Number, optional)
- `min_engagement_rate` (Number, optional)
- `max_age_days` (Number, optional)
- `active` (Checkbox, default True)

**Mapping to FilterRule**:
- Direct 1:1 field mapping
- Empty text fields ’ None in Python
- Unchecked checkbox ’ False in Python
- Missing number fields ’ None in Python

---

## Migration Notes

**No database migrations required** - Lark Base table will be manually created by user.

**Backward Compatibility**:
- Existing TikTokContent and MonitoringTarget models unchanged
- Adding FilterRule to existing models.py file (non-breaking addition)
- Existing pipeline code unaffected (filtering is opt-in via monitor.py changes)
