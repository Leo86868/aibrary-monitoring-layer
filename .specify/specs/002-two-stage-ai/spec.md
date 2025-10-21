# Feature Specification: Two-Stage AI Analysis Upgrade

**Feature Branch**: `001-two-stage-ai`
**Created**: 2025-10-19
**Status**: Draft
**Input**: User description: "Two-stage AI analysis upgrade for competitor intelligence with content-first relevance scoring and concise strategic insights"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Content-First Analysis (Priority: P1)

AIbrary monitoring system analyzes TikTok content based on WHAT the content is about rather than WHO posted it, providing accurate relevance scoring for learning/book-related content regardless of the creator.

**Why this priority**: This is the core problem - current system incorrectly scores OpenAI's learning content as low relevance just because OpenAI isn't a direct competitor. Content relevance should be topic-based.

**Independent Test**: Can be fully tested by analyzing mixed content from different creators and verifying relevance scores match content topics, not creator identity.

**Acceptance Scenarios**:

1. **Given** OpenAI posts "5 ways to read books faster", **When** system analyzes content, **Then** relevance score is 8-9/10 (high relevance to learning apps)
2. **Given** Blinkist posts "New AI features in our app", **When** system analyzes content, **Then** relevance score is 3-4/10 (tech features, not learning content)
3. **Given** any creator posts book/learning content, **When** system analyzes it, **Then** general analysis describes the content objectively

---

### User Story 2 - Cost-Efficient Single API Call (Priority: P1)

System performs both general content analysis and strategic evaluation in a single API call to minimize costs while maintaining analysis quality.

**Why this priority**: Cost optimization is critical for scaling the monitoring system. Two separate API calls would double the cost.

**Independent Test**: Can be tested by monitoring API call count and verifying both general analysis and strategic metrics are populated from one Gemini request.

**Acceptance Scenarios**:

1. **Given** any TikTok content, **When** system runs analysis, **Then** exactly one API call is made to Gemini
2. **Given** single API response, **When** system parses it, **Then** both general analysis and strategic fields are populated
3. **Given** analysis completes, **When** checking database, **Then** both "Analysis" column and strategic fields contain relevant data

---

### User Story 3 - Concise Strategic Insights (Priority: P2)

System provides brief, actionable strategic insights instead of verbose marketing jargon, focusing on what AIbrary can learn and apply.

**Why this priority**: Current insights are too wordy and full of jargon. Users need quick, actionable takeaways.

**Independent Test**: Can be tested by reviewing generated insights for length (under 500 characters) and actionability (contains specific recommendations).

**Acceptance Scenarios**:

1. **Given** well-performing content, **When** system generates insights, **Then** output is under 500 characters and contains specific actionable recommendations
2. **Given** strategic insights, **When** reviewing them, **Then** they focus on hook effectiveness, format choices, and specific tactics to adopt/avoid
3. **Given** insights for AIbrary team, **When** reading them, **Then** they contain no marketing jargon or unnecessary bullet points

---

### User Story 4 - Update Existing Records (Priority: P3)

System updates existing content records with new analysis instead of creating duplicates when re-analyzing content.

**Why this priority**: Prevents database pollution with duplicate records when re-running analysis on existing content.

**Independent Test**: Can be tested by running analysis twice on the same content_id and verifying only one record exists in database.

**Acceptance Scenarios**:

1. **Given** content already exists in database, **When** system analyzes it again, **Then** existing record is updated, not duplicated
2. **Given** re-analysis completes, **When** checking database, **Then** content_id appears only once with updated analysis fields

---

### Edge Cases

- What happens when content has no clear learning/book relevance (should score 0-1)?
- How does system handle API failures or rate limits during analysis?
- What happens when content_type cannot be determined from the response?
- How does system handle very short captions with minimal content?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST analyze content topics objectively before applying competitor intelligence scoring
- **FR-002**: System MUST generate both general content analysis and strategic evaluation in a single API call
- **FR-003**: System MUST score relevance based on content topics (books/learning/productivity) not creator identity
- **FR-004**: System MUST provide strategic insights in under 500 characters with specific actionable recommendations
- **FR-005**: System MUST update existing database records instead of creating duplicates
- **FR-006**: System MUST parse content_type correctly including values with underscores (e.g., "educational_tips")
- **FR-007**: System MUST include AIbrary company context in analysis prompt for accurate competitive positioning
- **FR-008**: System MUST save both general analysis (to "Analysis" column) and strategic fields (relevance_score, strategic_value, content_type, strategic_insights)

### Key Entities *(include if feature involves data)*

- **TikTokContent**: Enhanced with strategic analysis fields and content-first relevance scoring
- **AnalysisResult**: Modified to handle two-stage analysis output with simplified scoring metrics
- **AIbrary Context**: Company description and competitive positioning for accurate analysis

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Content relevance scoring accuracy improves - learning content scores 7-10/10 regardless of creator
- **SC-002**: API cost reduced by 50% through single-call two-stage analysis instead of separate calls
- **SC-003**: Strategic insights are 70% shorter (under 500 chars) while maintaining actionable value
- **SC-004**: Zero duplicate records created when re-analyzing existing content
- **SC-005**: Content_type parsing success rate improves to 95% for standard categories
- **SC-006**: Analysis completion time under 10 seconds per content item including database save

## Monitoring Strategy Context

**Current Scope:** This feature is optimized for **Competitor Intelligence** monitoring strategy.

The `COMPETITOR_INTELLIGENCE_PROMPT` in `src/analysis/prompts.py` is tailored for:
- Profile-based content from direct competitors (@openai, @blinkist_app, @headway.app)
- Topic relevance + execution quality scoring
- Marketing tactics analysis (what→why→try structure)

**Future Strategies:** When implementing Trend Discovery or Niche Deep-Dive strategies:
- Add strategy-specific prompts to `src/analysis/prompts.py`
- Implement prompt routing based on `monitoring_strategy` field in content
- Each strategy may need different scoring criteria and insight focus

## Assumptions

- AIbrary's competitive focus is on book/learning apps (Blinkist, Headway) not general AI companies
- Gemini 2.5-flash API can handle complex two-stage prompts in single calls
- Database field names match exactly: relevance_score, strategic_value, content_type, strategic_insights
- Current content volume allows for individual API calls per content item
- Team prefers actionable insights over comprehensive analysis reports