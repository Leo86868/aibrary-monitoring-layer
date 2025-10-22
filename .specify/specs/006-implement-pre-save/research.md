# Research: Pre-Save Quality Filtering System

**Feature**: 006-implement-pre-save
**Date**: 2025-10-21
**Phase**: 0 - Outline & Research

## Research Questions

### 1. Hierarchical Rule Matching Algorithm

**Question**: What's the most efficient algorithm for three-level hierarchical rule matching?

**Decision**: Use composite key tuple matching with specificity-ordered lookup

**Rationale**:
- Composite key tuples `(strategy, target_type, target_value)` provide O(1) dictionary lookups
- Specificity ordering (most specific first) ensures correct rule selection
- Python dict keys support tuples natively, no additional data structures needed
- Simple fallback chain: try (S,T,V) ’ try (S,T,None) ’ try (S,None,None)

**Alternatives Considered**:
- **Tree-based matching**: Hierarchical tree structure (strategy ’ type ’ target)
  - Rejected: More complex implementation, same O(1) performance, harder to debug
- **Rule priority scoring**: Assign numeric priorities to rules and select highest
  - Rejected: Requires manual priority management, less intuitive than specificity levels
- **Pattern matching with wildcards**: Use glob patterns like "Competitor Intelligence/profile/*"
  - Rejected: More flexible but slower (regex matching), overkill for 3-level hierarchy

**Implementation Notes**:
- Build dict during rule loading: `{(strategy, type, value): rule, ...}`
- Matching function tries 3 lookups in order, returns first match or None
- Empty string and None both treated as wildcard for target_value

---

### 2. Filter Logic: AND vs OR for Multiple Thresholds

**Question**: When a rule has multiple thresholds (min_likes, min_views, min_engagement_rate), should content pass if ALL thresholds are met (AND) or ANY threshold is met (OR)?

**Decision**: Use OR logic (content passes if ANY threshold is exceeded)

**Rationale**:
- OR logic is more permissive and reduces risk of accidentally filtering valuable content
- Different metrics capture different engagement patterns:
  - High views + low likes = broad reach but low resonance
  - Low views + high likes = niche but highly resonant
  - Both scenarios can be strategically valuable
- Easier to tune rules (adjust individual thresholds independently)
- Aligns with fail-open philosophy (prefer false positives over false negatives)

**Alternatives Considered**:
- **AND logic**: Content must exceed ALL thresholds
  - Rejected: Too restrictive, high risk of filtering valuable content
  - Example failure: Content with 100K views but 4K likes would be filtered if min_likes=5K
- **Weighted scoring**: Combine metrics into composite score
  - Rejected: Requires empirical weight tuning, adds complexity without clear benefit
- **Configurable per-rule**: Let each rule specify AND/OR logic
  - Rejected: Adds configuration complexity, most users wouldn't understand the distinction

**Implementation Notes**:
- Filter function checks each threshold independently
- Returns True if ANY threshold is exceeded (short-circuit evaluation)
- Missing metrics (None) treated as 0 (fail threshold checks)

---

### 3. Fail-Open vs Fail-Closed Design

**Question**: When filter rules cannot be loaded (Lark API down, network error), should the system save all content (fail-open) or save nothing (fail-closed)?

**Decision**: Fail-open (save all content on error)

**Rationale**:
- Primary purpose of filtering is cost optimization, not security
- Losing scraped content due to filtering error is worse than saving low-quality content
- Temporary Lark API outages shouldn't block the entire pipeline
- User can manually clean up low-quality content later, but lost scraping data is unrecoverable
- Aligns with existing system philosophy (prefer data over cleanliness)

**Alternatives Considered**:
- **Fail-closed**: Save nothing on error
  - Rejected: Data loss risk too high, defeats purpose of monitoring
- **Retry with exponential backoff**: Retry Lark API calls before failing
  - Rejected: Adds latency to pipeline, doesn't solve fundamental "what if still fails?" question
- **Cache rules locally**: Store last successful rule fetch on disk
  - Rejected: Stale rules could filter incorrectly, adds cache invalidation complexity

**Implementation Notes**:
- Wrap rule loading in try/except block
- On exception, log warning and return empty rule list
- Empty rule list triggers pass-all logic in filter function
- Metrics show "0 filtered (error: failed to load rules)" for visibility

---

### 4. Engagement Rate Calculation

**Question**: How should engagement_rate be calculated when not provided in scraped data?

**Decision**: Calculate as `(likes / views) * 100` with safe division (0 if views=0)

**Rationale**:
- Industry-standard formula for social media engagement
- Percentage format (0-100) is intuitive and easy to configure in Lark Base
- Likes-to-views ratio captures content resonance (not just reach)
- Safe division prevents ZeroDivisionError crashes

**Alternatives Considered**:
- **Include comments**: `((likes + comments) / views) * 100`
  - Rejected: Comments can inflate engagement unfairly (spam, bots)
- **Weighted formula**: `(likes * 0.7 + comments * 0.3) / views * 100`
  - Rejected: Arbitrary weights, no empirical basis for 0.7/0.3 split
- **Don't calculate**: Only use engagement_rate if provided by scraper
  - Rejected: TikTok API doesn't always provide engagement_rate field

**Implementation Notes**:
- Calculate during filtering if engagement_rate is None
- Use `engagement_rate = (likes / views * 100) if views > 0 else 0`
- Store calculated value back on TikTokContent object for reuse

---

### 5. Rule Caching Strategy

**Question**: Should filter rules be fetched once per pipeline run or once per target?

**Decision**: Fetch once per pipeline run and cache in memory

**Rationale**:
- Filter rules change infrequently (human-edited configuration)
- Fetching per-target wastes API calls (10+ targets × same rules = unnecessary load)
- In-memory cache is simple (just a list of FilterRule objects)
- Pipeline runs are short-lived (minutes), so stale cache is not a concern

**Alternatives Considered**:
- **Fetch per target**: Re-fetch rules for each monitoring target
  - Rejected: Wasteful API calls, no benefit (rules don't change mid-run)
- **Persistent cache**: Store rules in SQLite/JSON file between runs
  - Rejected: Adds staleness complexity, rules should be fresh each run
- **TTL-based cache**: Expire cached rules after N minutes
  - Rejected: Overkill for short pipeline runs

**Implementation Notes**:
- Fetch rules once in monitor.py before processing targets
- Pass rule list to filtering function for each target
- No need for thread-safety (single-threaded pipeline)

---

## Best Practices Research

### Python Dataclass Design

**Research Topic**: Best practices for immutable filter rules

**Findings**:
- Use `@dataclass(frozen=True)` for immutable rules (prevents accidental modification)
- Use `Optional[X]` for fields that can be None (target_value, threshold fields)
- Provide default values for optional fields to simplify construction
- Add `__post_init__` validation if needed (e.g., threshold >= 0)

**Application to Feature**:
```python
@dataclass(frozen=True)
class FilterRule:
    strategy: str
    target_type: Optional[str] = None
    target_value: Optional[str] = None
    min_likes: Optional[int] = None
    min_views: Optional[int] = None
    min_engagement_rate: Optional[float] = None
    max_age_days: Optional[int] = None
    active: bool = True
```

---

### Error Handling Patterns

**Research Topic**: Graceful degradation in data pipelines

**Findings**:
- Fail-open pattern: On non-critical errors, log warning and continue with degraded behavior
- Fail-fast pattern: On critical errors (data corruption), crash immediately with clear message
- Use specific exception types for different failure modes
- Always log errors with context (which rule, which content, what threshold)

**Application to Feature**:
- Filter rule loading: Fail-open (continue with no filtering)
- Rule matching: Fail-fast (crash if invalid rule format, indicates bug)
- Content filtering: Fail-open per-item (log warning, include item in output)

---

### Logging and Observability

**Research Topic**: Debugging hierarchical matching logic

**Findings**:
- Log rule selection decision for each content item at DEBUG level
- Log filtering metrics summary at INFO level (X scraped, Y filtered, Z saved)
- Include rule details in logs (which rule was matched, why content passed/failed)
- Use structured logging when possible (key=value format for easy parsing)

**Application to Feature**:
```python
# DEBUG level (per-item)
logger.debug(f"Content {content_id}: matched rule {rule} (specificity level 2)")
logger.debug(f"Content {content_id}: PASS (likes={likes} > min_likes={min_likes})")

# INFO level (summary)
logger.info(f"Filtering: {scraped} scraped ’ {saved} saved ({filtered} filtered out)")
```

---

## Technical Decisions Summary

| Decision | Choice | Key Rationale |
|----------|--------|---------------|
| Rule matching algorithm | Composite key tuple with specificity-ordered lookup | O(1) performance, simple implementation |
| Multi-threshold logic | OR (any threshold met) | More permissive, reduces false negatives |
| Error handling | Fail-open (save all on error) | Prefer data over cleanliness, avoid data loss |
| Engagement rate formula | (likes / views) * 100 | Industry standard, intuitive percentage |
| Rule caching | Once per pipeline run | Minimize API calls, rules change infrequently |
| Data structure | Frozen dataclass | Immutable rules, type safety, IDE support |

---

## Open Questions

**None** - All technical decisions resolved. Ready for Phase 1 (Design & Contracts).
