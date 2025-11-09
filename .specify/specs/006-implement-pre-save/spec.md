# Feature Specification: Pre-Save Quality Filtering System

**Feature Branch**: `006-implement-pre-save`
**Created**: 2025-10-21
**Status**: Draft
**Input**: User description: "Implement pre-save quality filtering system for scraped TikTok content using hierarchical rule matching"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Strategy-Level Quality Filtering (Priority: P1)

As a system operator, I want scraped TikTok content to be automatically filtered based on quality thresholds before saving to the database, so that only high-engagement content reaches AI analysis and reduces processing costs.

**Why this priority**: This is the foundation of the entire filtering system. Without basic filtering, low-quality content pollutes the database and wastes AI analysis credits. This story delivers immediate cost savings and database cleanliness.

**Independent Test**: Can be fully tested by adding one strategy-level filter rule (e.g., "Competitor Intelligence requires min 5000 likes") and running the monitoring pipeline. Success is measured by verifying that only content meeting the threshold is saved to the database.

**Acceptance Scenarios**:

1. **Given** a filter rule exists for "Competitor Intelligence" with min_likes=5000, **When** the system scrapes 10 videos (3 with >5000 likes, 7 with <5000 likes), **Then** only the 3 high-engagement videos are saved to the database
2. **Given** no filter rules exist in the database, **When** the system scrapes content, **Then** all scraped content is saved (fail-open behavior)
3. **Given** a filter rule has active=False, **When** the system loads filter rules, **Then** that rule is ignored and does not affect filtering
4. **Given** content has 4000 likes but 50000 views, and the rule requires min_likes=5000 OR min_views=10000, **When** filtering is applied, **Then** the content passes (OR logic - any threshold met)

---

### User Story 2 - Target-Type Specific Filtering (Priority: P2)

As a system operator, I want different quality thresholds for different target types (profiles vs hashtags), so that filtering accounts for the different engagement patterns of each source type.

**Why this priority**: Hashtags typically have noisier, lower-engagement content than curated profiles. Type-specific rules allow more aggressive filtering for hashtags while keeping reasonable thresholds for profiles. This improves filtering precision without losing valuable profile content.

**Independent Test**: Can be fully tested by adding two rules - one for "Niche Deep-Dive + profile" (min 5000 likes) and one for "Niche Deep-Dive + hashtag" (min 10000 likes). Scrape both profiles and hashtags, then verify each is filtered according to its type-specific rule.

**Acceptance Scenarios**:

1. **Given** rules exist for "Competitor Intelligence + profile" (min_likes=5000) and "Competitor Intelligence + hashtag" (min_likes=10000), **When** content is scraped from both @blinkist (profile) and #book (hashtag), **Then** profile content with 6000 likes is saved but hashtag content with 6000 likes is filtered out
2. **Given** a type-specific rule exists but no strategy-level rule exists, **When** matching rules for content, **Then** the type-specific rule is used (no fallback needed)
3. **Given** content from an unknown target type is scraped, **When** filtering is applied, **Then** the system falls back to strategy-level rules if available

---

### User Story 3 - Target-Specific Override Rules (Priority: P3)

As a system operator, I want to configure special quality thresholds for specific high-value targets (e.g., @blinkist, @notionhq), so that I can ensure complete coverage of VIP competitors even if their individual posts have lower engagement.

**Why this priority**: Some direct competitors are so strategically important that we want all their content regardless of engagement. This enables fine-grained control for VIP targets while maintaining general quality bars for others.

**Independent Test**: Can be fully tested by adding a target-specific rule for "@blinkist" (min_likes=1000) while keeping a general profile rule (min_likes=5000). Scrape @blinkist and another profile, then verify @blinkist content with 2000 likes is saved but other profiles need 5000+ likes.

**Acceptance Scenarios**:

1. **Given** rules exist for "Competitor Intelligence + profile + @blinkist" (min_likes=1000) and "Competitor Intelligence + profile" (min_likes=5000), **When** content from @blinkist is filtered, **Then** the target-specific rule (1000 likes) is used instead of the general rule
2. **Given** a target-specific rule exists for @blinkist, **When** content from @audiobooks (different target) is filtered, **Then** the target-specific rule is NOT applied to @audiobooks (only applies to exact match)
3. **Given** three rules exist at all specificity levels (strategy, type, target), **When** hierarchical matching occurs, **Then** the most specific matching rule is selected (target-specific > type-specific > strategy-level)

---

### User Story 4 - Filtering Metrics and Visibility (Priority: P4)

As a system operator, I want to see filtering metrics (total scraped, filtered out, saved) after each monitoring run, so that I can understand what content is being excluded and adjust rules if needed.

**Why this priority**: Visibility enables rule tuning and prevents accidentally filtering too aggressively. This is important for operational monitoring but not blocking for basic filtering functionality.

**Independent Test**: Can be fully tested by running the monitoring pipeline with filtering enabled and verifying that the terminal output shows: "X items scraped, Y filtered out, Z saved" with correct counts.

**Acceptance Scenarios**:

1. **Given** filtering rules are active, **When** the monitoring pipeline completes, **Then** the system reports total scraped count, filtered out count, and saved count
2. **Given** 100 items scraped and 30 filtered out, **When** metrics are reported, **Then** the numbers clearly show "100 scraped → 70 saved (30 filtered out)"
3. **Given** no items were filtered out, **When** metrics are reported, **Then** the system shows "X scraped → X saved (0 filtered out)" to confirm filtering ran but passed everything

---

### Edge Cases

- What happens when a filter rule has all thresholds set to 0? (Should pass all content for that rule)
- What happens when multiple rules at the same specificity level match? (Use first matching rule, deterministic ordering)
- How does the system handle corrupted or missing engagement data from scraping? (Treat missing metrics as 0, fail threshold checks)
- What happens if the Filter_Rules table cannot be accessed? (Fail-open: save all content and log warning)
- How does the system handle empty string target_value vs NULL? (Both treated as wildcard for type-level rules)
- What happens when engagement_rate is calculated but not in scraped data? (Calculate during filtering using likes/views formula)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST fetch active filter rules from Lark Base Filter_Rules table at the start of each monitoring pipeline run
- **FR-002**: System MUST support three-level hierarchical rule matching (strategy + target_type + target_value, strategy + target_type, strategy only)
- **FR-003**: System MUST select the most specific matching rule when multiple rules could apply to the same content
- **FR-004**: System MUST filter content using OR logic (content passes if ANY threshold is met - likes OR views OR engagement_rate)
- **FR-005**: System MUST ignore filter rules where active=False
- **FR-006**: System MUST save all scraped content if no matching filter rules are found (fail-open design)
- **FR-007**: System MUST save all scraped content if Filter_Rules table cannot be accessed (fail-open on error)
- **FR-008**: System MUST apply filtering AFTER scraping but BEFORE saving content to the database
- **FR-009**: System MUST track and report filtering metrics (total scraped, filtered out, saved) after each monitoring run
- **FR-010**: System MUST support filtering based on min_likes, min_views, min_engagement_rate, and max_age_days thresholds
- **FR-011**: System MUST calculate engagement_rate if not provided in scraped data (using formula: likes/views * 100)
- **FR-012**: System MUST treat missing engagement metrics (likes, views) as 0 when comparing against thresholds
- **FR-013**: System MUST preserve existing monitoring pipeline behavior (scrape → filter → save → analyze)
- **FR-014**: System MUST allow users to add, modify, or disable filter rules via Lark Base UI without code changes

### Key Entities *(include if feature involves data)*

- **FilterRule**: Represents a quality filtering rule with composite key (strategy, target_type, target_value) and threshold values (min_likes, min_views, min_engagement_rate, max_age_days). The active flag controls whether the rule is applied.

- **TikTokContent**: Existing entity representing scraped content. Used in filtering to compare engagement metrics (likes, views, engagement_rate, created_at) against FilterRule thresholds.

- **MonitoringTarget**: Existing entity representing a monitoring target. The strategy and target_type fields are used to match content to appropriate filter rules during hierarchical matching.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Filter rules can be added, modified, or disabled via Lark Base UI, and changes take effect in the next monitoring run without code deployment
- **SC-002**: Content is filtered before saving to the database, reducing database storage by at least 30% for high-volume sources (hashtags, search terms)
- **SC-003**: Hierarchical rule matching correctly selects the most specific rule 100% of the time (validated via unit tests)
- **SC-004**: System continues to save all content when filter rules are unavailable (fail-open), with no pipeline failures
- **SC-005**: Filtering metrics are displayed after each monitoring run, showing scraped vs saved counts
- **SC-006**: AI analysis costs are reduced by filtering out low-quality content before analysis phase
- **SC-007**: Existing Competitor Intelligence and Niche Deep-Dive workflows continue to function without modification
- **SC-008**: Content filtering completes in under 5 seconds for batches of 100 items

## Assumptions

- Lark Base Filter_Rules table will be manually created by the user with the specified schema (strategy, target_type, target_value, min_likes, min_views, min_engagement_rate, max_age_days, active)
- Filter rules use OR logic for thresholds (content passes if ANY metric exceeds threshold), not AND logic
- Engagement rate is defined as (likes / views) * 100 when calculated
- Target values must match exactly (case-sensitive) for target-specific rules to apply (@blinkist vs @Blinkist are different)
- Empty or NULL target_value in a rule indicates a wildcard (applies to all targets of that type)
- Filter rules are cached in memory for the duration of a single monitoring run (not re-fetched per target)
- max_age_days threshold requires content to have a created_at or published_at timestamp
- If multiple rules at the same specificity level match, the first rule found is used (deterministic based on database order)

## Dependencies

- Existing Lark Base API integration (LarkClient) for fetching filter rules
- Existing TikTokContent data model with engagement metrics (likes, views, engagement_rate)
- Existing MonitoringTarget data model with strategy field
- Existing monitoring pipeline in monitor.py that can be extended with filtering step

## Open Questions

None - specification is complete and ready for planning.
