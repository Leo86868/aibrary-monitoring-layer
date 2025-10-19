# TikTok Database Schema V1 - Comprehensive Design

**Date**: 2025-10-18
**Status**: First Version for Discussion
**Focus**: Multi-strategy TikTok monitoring with intelligent filtering

## Strategic Use Cases Analysis (Simplified)

### 1. Competitor Intelligence (Profile-based)
- **Target**: Specific creators (@openai, @nvidia, @anthropic)
- **Volume**: Low (10-20 recent posts per run)
- **Focus**: Creator performance, content strategy, audience engagement
- **Filtering**: High quality threshold, comprehensive metadata collection

### 2. Trend Discovery (Hashtag-based + Hot News)
- **Target**: Trending hashtags (#ai, #machinelearning, #gpt) + breaking news keywords
- **Volume**: High (100+ posts per run, filter to top 10%)
- **Focus**: Viral content identification, emerging narratives, breaking AI news
- **Filtering**: Engagement velocity, virality indicators, time-decay importance

### 3. Niche Deep-Dive (Specialized Communities)
- **Target**: Long-tail hashtags and specialized communities (#airesearch, #mlops, #aiethics)
- **Volume**: Medium (30-50 posts, higher quality threshold)
- **Focus**: Expert insights, technical discussions, specialized content
- **Filtering**: Authority scoring, content depth analysis

---

## Table 1: Monitoring_Targets (Strategic Configuration)

### Core Target Definition
- `target_id` (Auto Number, Primary Key)
- `platform` (Single Select: tiktok)
- `target_type` (Single Select: profile, hashtag, keyword, trending_discovery)
- `target_value` (Text, Required) - "@username", "#hashtag", "keyword phrase"

### Strategic Context
- `monitoring_strategy` (Single Select: competitor_intel, trend_discovery, niche_deep_dive)
- `strategic_priority` (Single Select: critical, high, medium, low)
- `collection_purpose` (Text) - "Monitor OpenAI content strategy", "Track AI breakthrough discussions"

### Volume & Quality Controls
- `results_limit` (Number) - **Strategy-dependent defaults:**
  - Competitor: 20
  - Trend Discovery: 100
  - Hot News: 50
  - Niche: 30
- `quality_threshold` (Single Select: minimal, standard, high, premium)
- `engagement_minimum` (Number) - Min engagement rate to collect
- `freshness_hours` (Number) - Only collect content from last X hours (hot news = 24, trends = 72)

### Processing Configuration
- `enable_transcription` (Checkbox) - Whisper API (cost consideration)
- `enable_ai_scoring` (Checkbox) - GPT-4o-mini relevance scoring
- `keyword_filter_list` (Text) - JSON array of must-have/exclude keywords
- `creator_authority_weight` (Number, 0-1) - How much creator reputation matters

### Operational
- `active` (Checkbox, Default: true)
- `last_processed` (DateTime)
- `next_scheduled` (DateTime)
- `processing_frequency` (Single Select: hourly, daily, weekly)
- `created_by` (Person)
- `team_notes` (Text, Multi-line)

---

## Table 2: TikTok_Content (Rich Metadata for Intelligent Filtering)

### Content Identity
- `content_id` (Text, Primary Key) - TikTok video ID
- `target_id` (Link to Monitoring_Targets) - **CRITICAL LINKAGE**
- `video_url` (URL, Required)
- `content_type` (Single Select: video, live, story) - Future TikTok formats

### Creator Intelligence
- `author_username` (Text)
- `author_display_name` (Text)
- `author_follower_count` (Number) - **Critical for authority scoring**
- `author_verified` (Checkbox)
- `author_bio` (Text) - For creator categorization
- `author_authority_score` (Number, 0-100) - **Calculated field**

### Content Analysis
- `caption` (Text, Multi-line)
- `hashtags` (Text) - JSON array - **Critical for trend analysis**
- `mentions` (Text) - JSON array
- `content_language` (Text) - Auto-detected language
- `video_duration` (Number, seconds) - **Important for transcription cost**
- `transcription` (Text, Multi-line) - Whisper API result
- `transcription_confidence` (Number, 0-1) - Quality score

### Engagement Metrics (Time-series for trend analysis)
- `likes` (Number)
- `shares` (Number)
- `comments` (Number)
- `views` (Number)
- `engagement_rate` (Number) - Calculated: (likes+comments+shares)/views
- `engagement_velocity` (Number) - Engagement per hour since posting
- `virality_score` (Number, 0-100) - **Calculated trending indicator**

### Content Classification
- `ai_relevance_score` (Number, 0-10) - GPT-4o-mini scoring
- `content_category` (Multi Select: educational, news, product_demo, opinion, entertainment)
- `technical_depth` (Single Select: basic, intermediate, advanced, expert)
- `sentiment` (Single Select: positive, neutral, negative)
- `keyword_matches` (Text) - JSON array of matched strategic keywords

### Strategic Value Assessment
- `strategic_value_score` (Number, 0-100) - **Composite scoring**
- `competitive_intel_value` (Number, 0-10) - Relevance for competitor analysis
- `trend_signal_strength` (Number, 0-10) - How much this indicates a trend
- `news_breaking_score` (Number, 0-10) - Timeliness and novelty

### Team Workflow
- `team_status` (Single Select: new, under_review, approved, high_priority, archived)
- `team_flags` (Multi Select: viral_potential, competitor_insight, breaking_news, deep_technical, follow_up_needed)
- `team_notes` (Text, Multi-line)
- `assigned_analyst` (Person) - For review workflow
- `review_deadline` (Date)

### Technical Metadata
- `sounds_used` (Text) - JSON array - For trend audio tracking
- `effects_used` (Text) - JSON array - TikTok effects metadata
- `video_thumbnail_url` (URL)
- `posting_timestamp` (DateTime) - **Critical for hot news**
- `discovered_timestamp` (DateTime) - When we found it
- `processed_timestamp` (DateTime) - When analysis completed

### Cost Tracking
- `transcription_cost` (Number) - Whisper API cost for this item
- `ai_scoring_cost` (Number) - GPT-4o-mini cost
- `total_processing_cost` (Number) - Sum of all AI costs

---

## Table 3: Content_Processing_Rules (Dynamic Filtering Logic)

### Rule Definition
- `rule_id` (Auto Number, Primary Key)
- `rule_name` (Text) - "High-Value Competitor Content", "Viral Trend Detection"
- `monitoring_strategy` (Single Select: competitor_intel, trend_discovery, niche_deep_dive)
- `rule_type` (Single Select: inclusion, exclusion, quality_boost, priority_flag)

### Filtering Criteria (JSON Configuration)
- `engagement_thresholds` (Text) - JSON: {"min_likes": 1000, "min_engagement_rate": 0.05}
- `creator_criteria` (Text) - JSON: {"min_followers": 10000, "verified_only": false}
- `content_criteria` (Text) - JSON: {"min_duration": 15, "max_duration": 180}
- `keyword_rules` (Text) - JSON: {"required": ["AI", "artificial intelligence"], "excluded": ["spam"]}
- `timing_rules` (Text) - JSON: {"max_age_hours": 48, "prefer_recent": true}

### Scoring Weights
- `relevance_weight` (Number, 0-1) - How much AI relevance matters
- `engagement_weight` (Number, 0-1) - How much engagement matters
- `authority_weight` (Number, 0-1) - How much creator authority matters
- `freshness_weight` (Number, 0-1) - How much recency matters

### Operational
- `active` (Checkbox)
- `created_by` (Person)
- `last_modified` (DateTime)

---

## Key Design Principles

### 1. Strategic Flexibility
- Same target can serve multiple strategies
- Configurable filtering per monitoring purpose
- Dynamic quality thresholds based on use case

### 2. Intelligent Volume Management
- High limits for trend discovery with aggressive filtering
- Lower limits for competitor monitoring with comprehensive analysis
- Cost-aware processing (transcription only for high-value content)

### 3. Multi-dimensional Scoring
- Not just "relevance" but strategic value for different purposes
- Composite scoring considering engagement, authority, timing, content quality
- Configurable weights per monitoring strategy

### 4. Rich Metadata for Analysis
- Creator authority and verification status
- Engagement velocity and virality indicators
- Content categorization and technical depth
- Strategic value assessment

### 5. Team Workflow Integration
- Review assignments and deadlines
- Status tracking and priority flagging
- Cost tracking for budget management

## Critical Discussion Points

1. **Complexity vs Usability**: Is this too complex for initial implementation?
2. **Cost Management**: How to balance rich metadata with processing costs?
3. **Data Volume**: How to handle 100+ posts per hashtag efficiently?
4. **Strategic Focus**: Which monitoring strategies should we prioritize first?
5. **Team Workflow**: What review processes do your 10 team members need?

**This is V1 - ready for your feedback and refinement.**