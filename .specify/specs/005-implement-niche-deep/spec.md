# Feature Specification: Niche Deep-Dive Monitoring Strategy

**Feature Branch**: `005-implement-niche-deep`
**Created**: 2025-10-21
**Status**: Draft
**Input**: User description: "Implement Niche Deep-Dive monitoring strategy for adjacent niche creator content in podcasts, books, learning, productivity, and AI-education spaces"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Adjacent Niche Creator Monitoring (Priority: P1)

Monitor adjacent niche creators and products in podcasts, productivity, learning, and knowledge management spaces to capture relevant content strategies and topic trends.

**Why this priority**: Core value proposition - adjacent niche profiles provide the highest relevance to AIbrary's market. Monitoring creators like @notionhq, @characterai, @elsaspeak, @ElevenLabs delivers immediate strategic value through niche-specific content insights.

**Independent Test**: Can be fully tested by configuring adjacent niche profile targets (@notionhq, @characterai) and verifying that relevant content is scraped, quality-filtered to best posts, and analyzed for niche category and content strategies.

**Acceptance Scenarios**:

1. **Given** adjacent niche profile targets configured (@notionhq, @characterai, @elsaspeak), **When** monitoring runs, **Then** system scrapes 30-50 recent TikTok videos from each creator
2. **Given** 30-50 scraped videos from creator, **When** quality filtering applies, **Then** system retains videos most relevant to AIbrary's niches (filters out off-topic/promotional posts)
3. **Given** filtered niche content, **When** AI analysis runs, **Then** each video gets assigned a niche_category and content strategy analysis
4. **Given** analyzed niche content, **When** saved to database, **Then** content is tagged with "Niche Deep-Dive" strategy and niche_category for grid view segmentation

---

### User Story 2 - Niche Hashtag Monitoring (Priority: P2)

Monitor niche-specific hashtags focused on AIbrary's adjacent content areas to discover relevant discussions and quality content in specific domains.

**Why this priority**: Complements profile monitoring with broader community content from specific niches. Hashtags like #AIed, #upskill, #habits capture focused discussions from diverse creators in AIbrary-adjacent spaces.

**Independent Test**: Can be tested independently by configuring niche hashtag targets (#AIed, #upskill, #habits) and verifying quality filtering produces niche-relevant content.

**Acceptance Scenarios**:

1. **Given** niche hashtag targets configured (#AIed, #upskill, #habits, book/podcast hashtags), **When** monitoring runs, **Then** system scrapes 50-100 TikTok videos per hashtag
2. **Given** 50-100 scraped hashtag videos, **When** quality filtering applies, **Then** system filters to 30-50 most niche-relevant videos (quality over quantity)
3. **Given** filtered niche content, **When** AI analysis runs, **Then** identifies niche_category, content strategies, and topic trends
4. **Given** niche content analyzed, **When** saved to database, **Then** content tagged with "Niche Deep-Dive" strategy and niche_category

---

### User Story 3 - Quality-First Filtering for Niche Relevance (Priority: P3)

Apply sophisticated quality filtering that prioritizes niche relevance and content strategy insights over engagement metrics to surface genuinely useful content.

**Why this priority**: Improves content utility. While engagement-based filtering works for viral content (Trend Discovery), Niche Deep-Dive requires filtering for niche relevance, strategic insights, and learning value.

**Independent Test**: Can be tested by comparing engagement-only filtering vs quality filtering on the same niche dataset and measuring niche relevance of results.

**Acceptance Scenarios**:

1. **Given** scraped content with varied niche relevance, **When** quality scoring calculates, **Then** score = f(niche_keywords, content_strategy_signals, relevance_to_AIbrary, engagement_patterns)
2. **Given** content with high engagement but off-topic, **When** quality penalty applies, **Then** content scores lower than moderate-engagement content with strong niche relevance
3. **Given** content with clear niche focus and strategic insights, **When** quality bonus applies, **Then** ranks higher than casual/generic content even with higher engagement
4. **Given** quality scores calculated, **When** top 30-50 filter applies, **Then** final set prioritizes niche relevance and strategic value over viral appeal

---

### User Story 4 - Niche Category Classification and Content Strategy Analysis (Priority: P3)

Analyze content for niche category, content strategies, and topic trends to identify truly valuable strategic insights for AIbrary.

**Why this priority**: Transforms filtered content into actionable intelligence. Distinguishes between different niche categories, identifies what content strategies work, and tracks topic trends across adjacent spaces.

**Independent Test**: Can be tested by reviewing AI analysis output for niche content and validating that insights identify niche category, content strategies, and topic trends.

**Acceptance Scenarios**:

1. **Given** niche TikTok content, **When** AI analyzes, **Then** assigns appropriate niche_category (Podcasts/Books/Productivity/AI-Ed/Upskilling/Knowledge Mgmt/Other)
2. **Given** niche content, **When** content strategy analysis runs, **Then** identifies hook types, format styles, and presentation strategies being used
3. **Given** niche content, **When** topic trend analysis runs, **Then** identifies specific topics/subjects being discussed (reading habits, productivity tips, etc.)
4. **Given** niche analysis complete, **When** insights extraction runs, **Then** provides 2-3 actionable content strategy insights or trend observations for AIbrary

---

### Edge Cases

- What happens when a niche creator profile has fewer than 30 videos total? (Cannot meet minimum threshold)
- What happens when niche hashtags return mostly off-topic content? (Quality filter threshold too strict?)
- How does system handle creators who post mix of niche-relevant and promotional content? (Need content-type filtering)
- What if "niche relevance" indicators miss content that's relevant but presented unconventionally?
- How to classify content that spans multiple niches (e.g., AI-powered productivity tool)?
- What if hashtags drift from niche focus over time (e.g., #upskill becomes generic career content)?
- How to handle niche content in languages other than English?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST scrape TikTok content from adjacent niche profile targets using existing Apify integration
- **FR-002**: System MUST scrape TikTok content from niche-specific hashtag targets using existing Apify integration
- **FR-003**: System MUST handle both profile targets (target_type="profile") and hashtag targets (target_type="hashtag")
- **FR-004**: System MUST retrieve sufficient items per target to enable quality filtering (50-100 items for hashtags, all recent for profiles)
- **FR-005**: System MUST calculate quality score for each scraped item using formula: quality_score = f(niche_keywords, content_strategy_signals, relevance_to_AIbrary, engagement_patterns)
- **FR-006**: System MUST filter content to 30-50 highest-quality items based on quality score (niche relevance + strategic value, not just engagement)
- **FR-007**: System MUST handle cases where fewer than 30 items meet quality threshold (take all that pass minimum bar)
- **FR-008**: System MUST tag all content with monitoring_strategy = "Niche Deep-Dive"
- **FR-009**: System MUST route "Niche Deep-Dive" content to specialized AI analysis prompt for niche assessment
- **FR-010**: AI analysis MUST assign niche_category (Podcasts & Audio | Books & Reading | Productivity & Habits | AI in Education | Upskilling & Career | Knowledge Management | Other)
- **FR-011**: AI analysis MUST identify content strategies (hook types, format styles, presentation approaches)
- **FR-012**: AI analysis MUST identify specific topic trends and subject matter
- **FR-013**: AI analysis MUST provide 2-3 actionable content strategy insights or trend observations per video
- **FR-014**: System MUST save analyzed content to Lark Base with Niche Deep-Dive strategy tag
- **FR-015**: System MUST NOT interfere with existing Competitor Intelligence or Trend Discovery workflows
- **FR-016**: System MUST filter out off-topic/promotional content from niche profiles (niche-relevant focus only)
- **FR-017**: System MUST extract same base engagement metrics as existing processors (likes, comments, views, engagement_rate)
- **FR-018**: System MUST extract video download URLs and subtitle URLs for AI analysis
- **FR-019**: System MUST filter out slideshow/photo content (videos only, same as other strategies)

### Key Entities

- **AdjacentNicheProfile**: Monitoring target with target_type="profile", target_value="@username" format, monitoring_strategy="Niche Deep-Dive", represents adjacent niche creator/product (e.g., @notionhq, @characterai, @elsaspeak)
- **NicheHashtag**: Monitoring target with target_type="hashtag", target_value="#hashtag" format, monitoring_strategy="Niche Deep-Dive", represents niche-specific topic focus (e.g., #AIed, #upskill, #habits)
- **QualityScore**: Composite metric prioritizing niche relevance, content strategy signals, AIbrary alignment, and engagement patterns
- **NicheContent**: TikTok content with monitoring_strategy="Niche Deep-Dive", quality_score, niche_category assignment
- **NicheCategory**: AI-assigned category field with values: Podcasts & Audio Learning | Books & Reading | Productivity & Habits | AI in Education | Upskilling & Career | Knowledge Management | Other

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: System successfully scrapes 30-50 recent videos from adjacent niche profile targets within 60 seconds
- **SC-002**: System successfully scrapes 50-100 items per niche hashtag target within 60 seconds
- **SC-003**: Quality filtering retains 30-50 highest-quality items that demonstrate niche relevance and strategic value
- **SC-004**: 80% of filtered content demonstrates clear relevance to AIbrary's niches (not off-topic/generic)
- **SC-005**: AI analysis completes for all filtered content within 15 minutes (same performance as other strategies)
- **SC-006**: AI analysis assigns niche_category for 100% of analyzed content
- **SC-007**: AI analysis identifies content strategies and topic trends with 90%+ consistency
- **SC-008**: System produces insights that inform AIbrary's content strategy decisions
- **SC-009**: Zero impact on existing Competitor Intelligence and Trend Discovery workflows (no performance degradation, no conflicts)
- **SC-010**: Content marked as "Niche Deep-Dive" routes to correct analysis prompt 100% of the time

## Assumptions

- **Profile Access**: Adjacent niche profiles remain public; if they go private, scraping fails gracefully
- **Content Volume**: Most niche creators have posted 30+ videos; if not, system takes all available niche-relevant content
- **Quality Indicators**: Niche relevance can be approximated from content keywords, topic focus, format patterns, engagement behavior
- **Niche Classification**: AI can assign niche_category from content analysis and context; manual override available if needed
- **Hashtag Relevance**: Niche hashtags maintain focus over time; periodic review needed if drift occurs
- **Content Language**: Analysis focuses on English content; multi-language support is out of scope
- **Strategic Value**: Can be inferred from content strategies, hook types, format choices, and topic selection
- **Gemini Capability**: Gemini 2.5 Flash can effectively assess niche relevance and content strategies (proven with Competitor Intelligence)
- **Filtering Threshold**: 30-50 items provides sufficient diversity while maintaining quality; future enhancement could make this configurable
- **Niche Category**: Can be classified from single scrape using content indicators and profile/hashtag context

## Dependencies

- **Feature 001 (TikTok Monitoring)**: Apify integration and Lark Base foundation
- **Feature 002 (Two-Stage AI)**: Gemini AI analysis framework
- **Feature 003 (Strategy Routing)**: monitoring_strategy field and routing logic already implemented
- **Existing ProfileProcessor**: Already implemented for Competitor Intelligence, reused for adjacent niche profiles
- **HashtagProcessor**: Needs implementation (shared with Feature 004 Trend Discovery)

## Technical Constraints

- Must reuse existing Apify TikTok actor (no custom scrapers)
- Must integrate with existing strategy routing (Feature 003) without modification
- Must use Gemini 2.5 Flash for analysis (same as other strategies)
- Must save to existing Lark Base tables (minimal schema changes: add niche_category column)
- Must maintain < $50/month combined cost across all strategies
- ProfileProcessor already exists; HashtagProcessor needs implementation but follows same pattern
