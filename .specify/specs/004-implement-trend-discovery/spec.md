# Feature Specification: Trend Discovery Monitoring Strategy

**Feature Branch**: `004-implement-trend-discovery`
**Created**: 2025-10-21
**Status**: Draft
**Input**: User description: "Implement Trend Discovery monitoring strategy for viral content in learning, books, productivity, and podcast spaces"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Viral Content Discovery via Hashtags (Priority: P1)

Monitor broad market hashtags in books, learning, productivity, and podcasts to identify trending, viral content that's capturing mass attention right now.

**Why this priority**: Core value proposition - hashtag monitoring provides the highest volume of trending content and is the primary mechanism for trend discovery in AIbrary's market. This alone delivers immediate value.

**Independent Test**: Can be fully tested by configuring hashtag targets (#books, #reading, #productivity, #learning, #podcasts) and verifying that viral content is scraped, filtered to top performers, and analyzed for viral signals.

**Acceptance Scenarios**:

1. **Given** hashtag targets configured (#books, #reading, #productivity, #learning, #podcasts), **When** monitoring runs, **Then** system scrapes 100+ TikTok videos for each hashtag
2. **Given** 100+ scraped videos, **When** viral filtering applies, **Then** system identifies and retains top 10% most viral content (10-15 videos)
3. **Given** filtered viral content, **When** AI analysis runs, **Then** each video gets viral signal strength score and narrative detection
4. **Given** analyzed content, **When** saved to database, **Then** content is tagged with "Trend Discovery" strategy for proper routing

---

### User Story 2 - Trending Topic Keyword Monitoring (Priority: P2)

Monitor trending topics and viral keywords to catch emerging trends in books, learning, and productivity before they become mainstream.

**Why this priority**: Complements hashtag monitoring with more specific, time-sensitive content. Catches trending book releases, viral productivity methods, and learning challenges that may not yet have established hashtags.

**Independent Test**: Can be tested independently by configuring search term targets ("Atomic Habits challenge", "best productivity tips 2024", "book recommendations") and verifying early detection of trending topics.

**Acceptance Scenarios**:

1. **Given** search keyword targets configured ("Atomic Habits challenge", "book summary tips"), **When** monitoring runs, **Then** system searches TikTok for keyword matches
2. **Given** search results returned, **When** recency filtering applies, **Then** prioritize content from last 7 days
3. **Given** recent keyword content, **When** viral filtering applies, **Then** identify rapid-growth content even if total engagement is still building
4. **Given** early-stage viral content, **When** analyzed, **Then** AI detects emerging narrative and trend velocity (accelerating vs fading)

---

### User Story 3 - Composite Viral Scoring and Intelligent Filtering (Priority: P3)

Apply sophisticated viral scoring that combines recency, engagement, and velocity to surface genuinely trending content.

**Why this priority**: Improves signal-to-noise ratio. While basic filtering works, composite scoring dramatically improves quality by catching early-stage viral content and filtering out old popular content.

**Independent Test**: Can be tested by comparing simple engagement filtering vs composite scoring on the same dataset and measuring precision of "truly viral" content identification.

**Acceptance Scenarios**:

1. **Given** scraped content with varied ages and engagement, **When** composite score calculates, **Then** score = f(recency_score, engagement_score, velocity_score)
2. **Given** content with high total engagement but posted 60+ days ago, **When** recency penalty applies, **Then** content scores lower than recent content with moderate engagement
3. **Given** content with rapidly growing engagement (high velocity), **When** velocity bonus applies, **Then** emerging viral content ranks higher than steady-state popular content
4. **Given** composite scores calculated, **When** top 10% filter applies, **Then** final set contains mix of established viral content and emerging trends

---

### User Story 4 - Viral Pattern Recognition and Narrative Analysis (Priority: P3)

Analyze why content is trending, what narrative is resonating, and provide actionable competitive insights.

**Why this priority**: Transforms raw viral content into strategic intelligence. Without this, we know what's viral but not why it matters or what to learn from it.

**Independent Test**: Can be tested by reviewing AI analysis output for viral content and validating that insights explain viral mechanics and provide actionable takeaways.

**Acceptance Scenarios**:

1. **Given** viral TikTok content, **When** AI analyzes, **Then** identifies specific viral hooks (emotional appeal, controversial take, breaking news, etc.)
2. **Given** multiple videos on same topic, **When** narrative analysis runs, **Then** detects common narrative threads and angles that resonate
3. **Given** trend velocity data, **When** trend lifecycle analysis runs, **Then** classifies as emerging/peaking/fading trend
4. **Given** viral content and competitive context, **When** competitive insight extraction runs, **Then** provides 2-3 actionable takeaways for our content strategy

---

### Edge Cases

- What happens when a hashtag returns fewer than 10 results? (Cannot filter to top 10%)
- What happens when all scraped content is very old (30+ days)? (Recency penalty too severe?)
- How does system handle duplicate content across multiple hashtags/searches?
- What if a "breaking news" keyword becomes outdated after several runs? (Need keyword rotation?)
- How to handle seasonal trends (e.g., content trending but only because it's holiday-related)?
- What if engagement metrics are missing or zero for some content?
- How to distinguish between genuinely viral content vs artificially boosted/bot-driven engagement?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST scrape TikTok content from hashtag targets using existing Apify integration
- **FR-002**: System MUST scrape TikTok content from search keyword targets using existing Apify integration
- **FR-003**: System MUST handle both hashtag targets (target_type="hashtag") and search targets (target_type="search")
- **FR-004**: System MUST retrieve minimum 100 items per hashtag/search target before filtering
- **FR-005**: System MUST calculate composite viral score for each scraped item using formula: viral_score = f(recency_days, engagement_rate, engagement_velocity)
- **FR-006**: System MUST filter scraped content to top 10% based on composite viral score
- **FR-007**: System MUST handle cases where fewer than 10 items are scraped (skip percentage filtering, take all)
- **FR-008**: System MUST tag all content with monitoring_strategy = "Trend Discovery"
- **FR-009**: System MUST route "Trend Discovery" content to trend-specific AI analysis prompt
- **FR-010**: AI analysis MUST identify viral signal strength (why content is trending)
- **FR-011**: AI analysis MUST detect narrative themes and angles resonating with audience
- **FR-012**: AI analysis MUST classify trend lifecycle stage (emerging/peaking/fading)
- **FR-013**: AI analysis MUST provide 2-3 actionable content strategy insights per viral video
- **FR-014**: System MUST save analyzed content to Lark Base with Trend Discovery strategy tag
- **FR-015**: System MUST NOT interfere with existing Competitor Intelligence workflow
- **FR-016**: System MUST handle duplicate content detection across multiple targets
- **FR-017**: System MUST filter out slideshow/photo content (videos only, same as Competitor Intelligence)
- **FR-018**: System MUST extract same engagement metrics as existing processors (likes, comments, views, engagement_rate)
- **FR-019**: System MUST extract video download URLs and subtitle URLs for AI analysis

### Key Entities

- **HashtagTarget**: Monitoring target with target_type="hashtag", target_value="#books" or "#reading" or "#productivity" format, monitoring_strategy="Trend Discovery"
- **SearchTarget**: Monitoring target with target_type="search", target_value="Atomic Habits challenge" or "best book recommendations 2024" format, monitoring_strategy="Trend Discovery"
- **ViralScore**: Composite metric combining recency penalty, engagement metrics, and velocity calculation
- **TrendContent**: TikTok content with monitoring_strategy="Trend Discovery", viral_score, trend_lifecycle stage
- **TrendNarrative**: AI-detected theme/angle explaining why content resonates in books/learning/productivity market (extracted from analysis)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: System successfully scrapes 100+ items per hashtag target within 60 seconds
- **SC-002**: System successfully scrapes 100+ items per search keyword target within 60 seconds
- **SC-003**: Viral filtering reduces 100+ items to 10-15 highest-quality viral items (top 10%)
- **SC-004**: 90% of filtered content is less than 14 days old (recency filtering works)
- **SC-005**: AI analysis completes for all filtered content within 15 minutes (same performance as Competitor Intelligence)
- **SC-006**: AI analysis identifies specific viral hooks for 100% of analyzed content
- **SC-007**: AI analysis detects narrative themes with 80%+ consistency across similar content
- **SC-008**: System produces actionable insights that inform content strategy decisions
- **SC-009**: Zero impact on existing Competitor Intelligence workflow (no performance degradation, no conflicts)
- **SC-010**: Content marked as "Trend Discovery" routes to correct analysis prompt 100% of the time

## Assumptions

- **Apify Configuration**: Same Apify TikTok actor supports both hashtag and search scraping (just different input parameters)
- **Volume**: Most broad hashtags (#books, #reading, #productivity, #learning, #podcasts) will return 100+ results; if not, system gracefully handles smaller datasets
- **Velocity Calculation**: Approximated using publish_date and current engagement (actual velocity tracking would require multiple scrapes over time)
- **Engagement Authenticity**: Apify-provided engagement metrics are reasonably accurate; bot detection is out of scope
- **Hashtag Format**: Users enter hashtags with # prefix (#books not books)
- **Search Keywords**: Keywords are English language (e.g., "Atomic Habits challenge", "best productivity tips"); multi-language support is out of scope
- **Content Freshness**: TikTok API provides publish dates; if missing, content is skipped
- **Analysis Language**: Gemini 2.5 Flash can effectively analyze viral patterns and narratives in books/learning/productivity market (proven with Competitor Intelligence)
- **Filtering Threshold**: 10% is appropriate for most use cases; future enhancement could make this configurable
- **Trend Lifecycle**: Can be approximated from single scrape using engagement trajectory patterns

## Dependencies

- **Feature 001 (TikTok Monitoring)**: Apify integration and Lark Base foundation
- **Feature 002 (Two-Stage AI)**: Gemini AI analysis framework
- **Feature 003 (Strategy Routing)**: monitoring_strategy field and routing logic already implemented
- **Existing ProfileProcessor**: HashtagProcessor and SearchProcessor will follow same pattern

## Technical Constraints

- Must reuse existing Apify TikTok actor (no custom scrapers)
- Must integrate with existing strategy routing (Feature 003) without modification
- Must use Gemini 2.5 Flash for analysis (same as Competitor Intelligence)
- Must save to existing Lark Base tables (no schema changes)
- Must maintain < $50/month combined cost across all strategies
