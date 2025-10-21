# Feature Specification: Strategy-Aware Analysis Routing

**Feature Branch**: `003-strategy-routing`
**Created**: 2025-10-20
**Status**: Draft
**Input**: User description: "Strategy-aware AI analysis routing to gracefully skip non-competitor content and enable future multi-strategy prompts"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Graceful Skipping for Non-Competitor Content (Priority: P1)

System analyzes only Competitor Intelligence content and gracefully skips Trend Discovery and Niche Deep-Dive content without errors, providing clear feedback about what was skipped and why.

**Why this priority**: User is populating the database with mixed-strategy content (competitors, trends, niche topics), but only Competitor Intelligence prompts are implemented. System must not fail or produce incorrect analysis for other strategies.

**Independent Test**: Can be fully tested by creating content records with different monitoring_strategy values and verifying only Competitor Intelligence content is analyzed.

**Acceptance Scenarios**:

1. **Given** content with monitoring_strategy="Competitor Intelligence", **When** system runs analysis, **Then** content is analyzed using COMPETITOR_INTELLIGENCE_PROMPT
2. **Given** content with monitoring_strategy="Trend Discovery", **When** system runs analysis, **Then** analysis is skipped with message "⏭️ Skipping (Trend Discovery prompt not implemented)"
3. **Given** content with monitoring_strategy="Niche Deep-Dive", **When** system runs analysis, **Then** analysis is skipped with message "⏭️ Skipping (Niche Deep-Dive prompt not implemented)"
4. **Given** batch of 10 mixed-strategy content items (7 Competitor, 2 Trend, 1 Niche), **When** batch analysis completes, **Then** summary shows "7 analyzed, 3 skipped"

---

### User Story 2 - Strategy Field Reading from Lark Base (Priority: P1)

System reads the monitoring_strategy field from TikTok Content table (populated via Lark Base lookup) and uses it for routing decisions.

**Why this priority**: Without reading the monitoring_strategy field from Lark, the routing logic cannot function. This is the foundational capability.

**Independent Test**: Can be tested by verifying the monitoring_strategy field is correctly read from Lark Base and accessible in the TikTokContent object.

**Acceptance Scenarios**:

1. **Given** content record in Lark Base with monitoring_strategy lookup populated, **When** system retrieves content, **Then** TikTokContent.monitoring_strategy contains correct value
2. **Given** content with no monitoring_strategy (lookup failed), **When** system attempts analysis, **Then** warning is logged and content is skipped
3. **Given** newly scraped content, **When** saved to Lark Base, **Then** monitoring_strategy lookup auto-populates based on Target link

---

### User Story 3 - Future-Ready Architecture for Multi-Strategy Prompts (Priority: P2)

System architecture supports easy addition of new strategy-specific prompts (Trend Discovery, Niche Deep-Dive) without modifying core routing logic.

**Why this priority**: Ensures the implementation is scalable and won't require refactoring when adding new strategies.

**Independent Test**: Can be tested by adding a new strategy prompt and verifying only routing configuration needs to change, not core logic.

**Acceptance Scenarios**:

1. **Given** developer adds TREND_DISCOVERY_PROMPT, **When** routing case is added for "Trend Discovery", **Then** system automatically routes Trend Discovery content to new prompt
2. **Given** three different strategy prompts exist, **When** analyzing mixed content, **Then** each content type is routed to its specific prompt
3. **Given** new strategy is added, **When** reviewing code changes, **Then** only prompt definition and routing case are modified

---

### User Story 4 - Clear Analysis Metrics and Logging (Priority: P3)

System provides clear visibility into which content was analyzed vs skipped, with strategy-specific metrics.

**Why this priority**: Helps user understand system behavior and verify routing is working correctly.

**Independent Test**: Can be tested by reviewing console output and verifying metrics match actual content processing.

**Acceptance Scenarios**:

1. **Given** batch analysis completes, **When** reviewing logs, **Then** each content item shows strategy and action taken (analyzed/skipped)
2. **Given** analysis summary, **When** displayed to user, **Then** shows count by strategy (e.g., "Competitor: 7 analyzed, Trend: 2 skipped, Niche: 1 skipped")
3. **Given** content skipped due to unimplemented strategy, **When** logged, **Then** message explains why and suggests future implementation

---

### Edge Cases

- What happens when monitoring_strategy field is None or empty (lookup failed)?
- What happens when monitoring_strategy contains an unknown value not in ["Competitor Intelligence", "Trend Discovery", "Niche Deep-Dive"]?
- What happens when content has monitoring_strategy but the corresponding prompt doesn't exist yet?
- How does the system behave during the transition period when adding a new strategy prompt?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST read monitoring_strategy field from TikTokContent objects retrieved from Lark Base
- **FR-002**: System MUST route content to appropriate analysis method based on monitoring_strategy value
- **FR-003**: System MUST analyze content with monitoring_strategy="Competitor Intelligence" using existing COMPETITOR_INTELLIGENCE_PROMPT
- **FR-004**: System MUST gracefully skip content with monitoring_strategy="Trend Discovery" with informative message
- **FR-005**: System MUST gracefully skip content with monitoring_strategy="Niche Deep-Dive" with informative message
- **FR-006**: System MUST log warning and skip content when monitoring_strategy is None or empty
- **FR-007**: System MUST provide batch analysis summary showing count of analyzed vs skipped items by strategy
- **FR-008**: System MUST support easy addition of new strategy prompts without modifying core routing logic
- **FR-009**: System MUST NOT fail or throw errors when encountering unimplemented strategy types
- **FR-010**: System MUST maintain backward compatibility with existing analyze_content() API

### Key Entities *(include if feature involves data)*

- **TikTokContent.monitoring_strategy**: Field populated via Lark Base lookup, drives routing decisions
- **VideoAnalyzer routing logic**: Strategy-aware routing in analyze_content() and batch_analyze() methods
- **Strategy prompts**: COMPETITOR_INTELLIGENCE_PROMPT (exists), TREND_DISCOVERY_PROMPT (future), NICHE_DEEPDIVE_PROMPT (future)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of Competitor Intelligence content is analyzed successfully
- **SC-002**: 0 errors or exceptions when processing Trend Discovery or Niche Deep-Dive content (graceful skipping)
- **SC-003**: Analysis summary accurately reports count of analyzed vs skipped items by strategy
- **SC-004**: monitoring_strategy field is successfully read from Lark Base for all retrieved content
- **SC-005**: Adding a new strategy prompt requires changes to only 2 locations (prompt definition + routing case)
- **SC-006**: No backward compatibility breaks - existing code continues to work with new routing logic

## Dependencies

- **Feature 001**: TikTok Content Monitoring - monitoring_strategy field exists in Lark Base
- **Feature 002**: Two-Stage AI Analysis - COMPETITOR_INTELLIGENCE_PROMPT implemented and working
- **Lark Base Configuration**: monitoring_strategy lookup field correctly configured with condition `target_value is Target`

## Assumptions

- monitoring_strategy field is already configured in Lark Base and working via lookup
- Only Competitor Intelligence strategy has implemented prompts currently
- Trend Discovery and Niche Deep-Dive prompts will be implemented in future features
- TikTokContent dataclass can be extended with monitoring_strategy field without breaking existing code
- Current content volume allows for sequential processing (no batch API optimization needed yet)

## Future Enhancements

- Implement TREND_DISCOVERY_PROMPT for viral content analysis
- Implement NICHE_DEEPDIVE_PROMPT for expert content analysis
- Add strategy-specific scoring metrics (different criteria for each strategy)
- Add configurable strategy routing (allow users to customize which strategies to analyze)
- Add analytics dashboard showing content distribution across strategies
