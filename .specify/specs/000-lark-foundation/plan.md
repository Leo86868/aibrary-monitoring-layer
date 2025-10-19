# Implementation Plan: Lark Base Foundation

**Feature**: 000-lark-foundation
**Created**: 2025-10-18
**Status**: Ready for Implementation
**Approach**: TikTok-First with Hybrid Architecture

## Technical Implementation Strategy

### Phase 1: Core Lark Tables (Day 1)

#### 1.1 Access Lark Base
- **Target**: Lark Base `Qr40bFHf8aKpBosZjXbcjF4rnXe`
- **Validation**: Confirm team access and permissions
- **Prerequisites**: Lark credentials configured

#### 1.2 Create Monitoring_Targets Table
**Schema Design**:
```
Table: Monitoring_Targets
Fields:
- target_id (Auto Number, Primary Key)
- platform (Single Select: tiktok, instagram, linkedin, rss)
- target_type (Single Select: profile, hashtag, keyword, url, company)
- target_value (Text, Required)
- active (Checkbox, Default: true)
- quality_preset (Single Select: low, medium, high)
- config_link (Link to Platform_Configs, Optional)
- results_limit (Number, Default: 20)
- team_notes (Text, Multi-line)
- created_by (Person)
- created_date (Created Time)
- last_modified (Last Modified Time)
```

#### 1.3 Create TikTok_Content Table
**Schema Design**:
```
Table: TikTok_Content
Fields:
- content_id (Text, Primary Key, TikTok Video ID)
- target_id (Link to Monitoring_Targets)
- video_url (URL, Required)
- author_username (Text)
- caption (Text, Multi-line)
- likes (Number)
- shares (Number)
- comments (Number)
- views (Number)
- video_duration (Number, seconds)
- sounds_used (Text, JSON array)
- hashtags (Text, JSON array)
- mentions (Text, JSON array)
- transcription (Text, Multi-line, Whisper result)
- ai_relevance_score (Number, 0-10)
- keyword_matches (Text, JSON array)
- team_flags (Multi Select: high_value, needs_review, viral, educational)
- team_notes (Text, Multi-line)
- discovered_date (Date)
- processed_date (Last Modified Time)
```

#### 1.4 Create Platform_Configs Table
**Schema Design**:
```
Table: Platform_Configs
Fields:
- config_id (Auto Number, Primary Key)
- platform (Single Select: tiktok, instagram, linkedin, rss)
- config_name (Text, e.g., "TikTok High Engagement")
- config_json (Text, Multi-line, JSON configuration)
- description (Text, Multi-line)
- created_by (Person)
- active (Checkbox)
- created_date (Created Time)
```

### Phase 2: TikTok Integration Architecture (Day 2-3)

**Note**: Detailed TikTok implementation moved to `001-tiktok-monitoring/` specs

#### 2.1 TikTok Strategic Monitoring Types
1. **Competitor Intelligence** (profiles) - 20 posts, high quality
2. **Trend Discovery** (hashtags + hot news) - 100+ posts, viral detection
3. **Niche Deep-Dive** (specialized communities) - 30-50 posts, expert content

#### 2.2 Lightweight Processing Module Design
**Alternative to Heavy n8n Workflows**:

```javascript
// Modular, Event-Driven Architecture
TikTokProcessor {
  - ConfigLoader (reads from Lark Platform_Configs)
  - TargetReader (reads from Monitoring_Targets)
  - ApifyConnector (TikTok scraping)
  - ValidationPipeline (4-layer filtering)
  - LarkWriter (writes to TikTok_Content)
}
```

**Processing Flow**:
1. **Config Loading**: Dynamic configuration from Lark
2. **Target Processing**: Read active TikTok targets
3. **Content Scraping**: Apify TikTok scraper
4. **Validation Pipeline**: 4-layer filtering
5. **Content Storage**: Write validated content to Lark

#### 2.3 API Integration Points
**Lark API Configuration**:
- **Base ID**: `Qr40bFHf8aKpBosZjXbcjF4rnXe`
- **App ID**: `cli_a860785f5078100d`
- **App Secret**: `sfH5BBpCd6tTeqfPB1FRlhV3JQ6M723A`
- **Tables**: Monitoring_Targets, TikTok_Content, Content_Processing_Rules
- **Rate Limits**: 20 requests/second

**Apify Integration**:
- **Actor**: `clockworks/tiktok-scraper`
- **Input**: TikTok profile/hashtag URLs
- **Output**: Video metadata + engagement metrics
- **Cost**: ~$0.01 per video processed

**OpenAI Integration**:
- **Whisper API**: Video transcription
- **GPT-4o-mini**: Relevance scoring
- **Cost**: $0.006/minute + $0.0001/item

### Phase 3: Team Workflow Testing (Day 4-5)

#### 3.1 Test Data Setup
**Initial Test Target**:
```
platform: tiktok
target_type: profile
target_value: @openai
active: true
quality_preset: medium
results_limit: 10
team_notes: "Initial test - OpenAI official account"
```

#### 3.2 Manual Team Workflow
**10-Person Team Process**:
1. **Input**: Team members add targets via Lark interface
2. **Processing**: Automated TikTok module processes targets
3. **Review**: Team reviews results in TikTok_Content table
4. **Annotation**: Team adds flags and notes for high-value content
5. **Iteration**: Adjust quality presets based on results

#### 3.3 Performance Validation
**Success Metrics**:
- Process 10 TikTok videos in <5 minutes
- 95%+ transcription accuracy for clear audio
- <$5 total cost for test run
- Zero data loss in Lark tables
- Team can add targets without technical support

## Technology Stack Implementation

### Core Technologies
- **Database**: Lark Base (existing Base ID)
- **Processing**: Node.js scripts (lightweight, modular)
- **APIs**: Lark, Apify, OpenAI
- **Configuration**: JSON-based, stored in Lark

### Development Environment
- **Local Development**: Node.js scripts on localhost
- **Configuration**: Environment variables for API keys
- **Version Control**: Git for scripts and configurations
- **Deployment**: Manual execution initially, automation later

### Security Implementation
- **API Keys**: Environment variables only
- **Lark Access**: Team-based permissions
- **Data Privacy**: No PII storage outside Lark
- **Audit Trail**: All changes tracked in Lark

## Risk Mitigation

### Technical Risks
- **Lark API Limits**: Implement exponential backoff
- **Apify Rate Limits**: Queue management with delays
- **TikTok Anti-Bot**: Use Apify's managed anti-detection
- **Cost Overruns**: Set daily spending limits

### Team Workflow Risks
- **Data Entry Errors**: Validation rules in Lark fields
- **Permission Issues**: Clear role definitions
- **Training Needs**: Document manual workflow steps
- **Scale Challenges**: Test with 1 target, gradually increase

## Next Steps for Implementation

1. **Create Lark tables** (manual setup in Lark interface)
2. **Configure API credentials** (environment setup)
3. **Build TikTok processing module** (Node.js script)
4. **Test with 1 target** (validate end-to-end flow)
5. **Team workflow training** (10-person team onboarding)

**Ready to proceed with implementation when approved.**