# AIbrary - Multi-Strategy TikTok Monitoring System

A scalable, specification-driven TikTok monitoring system with multi-strategy monitoring, AI-powered analysis, and quality filtering. Built with Python, Lark Base integration, and Apify scraping - designed for cost-effective content analysis under $50/month.

[![SpecKit](https://img.shields.io/badge/Development-SpecKit-blue)]()
[![Python](https://img.shields.io/badge/Runtime-Python_3.13-green)]()
[![Lark](https://img.shields.io/badge/Database-Lark_Base-00d5c4)]()
[![TikTok](https://img.shields.io/badge/Platform-TikTok-000000)]()

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config/.env.example config/.env
# Edit config/.env with your Apify token and Gemini API key

# Run the monitor
python3 src/run_monitoring.py
```

**Expected Output**:
```
🚀 Starting TikTok monitoring run...
📋 Loading active targets from Lark...
   Found 3 active targets
[1/3] Processing @elsaspeak (Niche Deep-Dive)...
✅ Scraped 30 items → Filtered to 16 items (46.7% filtered out)
💾 Saved 16 new items to Lark Base
🤖 Analyzing 16 Niche Deep-Dive items...
✅ Analysis complete!
```

## 🎯 What is AIbrary?

A **comprehensive TikTok monitoring system** with multi-strategy monitoring capabilities:

### Core Features (Features 001-006 Complete)
- ✅ **Multi-Strategy Monitoring** - Track competitors, trends, and niche content
  - Competitor Intelligence: Monitor direct competitors (@blinkist, @headway)
  - Niche Deep-Dive: Learn from adjacent niches (@notionhq, #book, #productivity)
  - Trend Discovery: Infrastructure ready for viral content detection
- ✅ **Profile & Hashtag Monitoring** - ProfileProcessor and HashtagProcessor working
- ✅ **Quality Filtering System** - Pre-save filtering with hierarchical rule matching
  - OR logic thresholds (likes, views, engagement rate, age)
  - 46.7% filter rate in production (reduces database noise)
  - Rules loaded from Lark Base Filter_Rules table
- ✅ **Strategy-Aware AI Analysis** - Different prompts for different strategies
  - Competitor Intelligence: Product/marketing insights
  - Niche Deep-Dive: Content strategy analysis (hooks, formats, engagement)
  - Video + subtitle analysis with Gemini 2.5 Flash
- ✅ **Niche Category Classification** - 7 categories for adjacent niche content
- ✅ **Lark Base Integration** - Team collaboration with automatic strategy propagation
- ✅ **Cost-Effective** - ~$5.50/month actual costs (well under $50 budget)
- ✅ **SpecKit Compliant** - Specification-driven development workflow

---

## 🏗️ Architecture

**Three-Layer System:**
- **Layer 1 (Monitoring)**: `src/layer1_monitoring/` - Scraping + Filtering
- **Layer 2 (Analysis)**: `src/layer2_analysis/` - AI-powered video analysis
- **Layer 3 (AIGC)**: `src/layer3_aigc/` - Content generation (planned)

### 6-Step Pipeline (Layers 1 + 2 Complete & Working)

```
1️⃣ LOAD TARGETS
   📥 Lark Base → Monitoring_Targets table
   ├─ target_value: @username or #hashtag
   ├─ target_type: profile or hashtag
   ├─ monitoring_strategy: Competitor Intelligence / Niche Deep-Dive
   └─ active: ✓

   ↓

2️⃣ PROCESSOR ROUTING
   ⚡ ProcessorFactory routes by target_type
   ├─ ProfileProcessor: @username → Apify profile scraping
   ├─ HashtagProcessor: #hashtag → Apify hashtag scraping
   └─ SearchProcessor: keywords (planned)

   ↓

3️⃣ SCRAPE CONTENT
   🎯 Apify TikTok Actor (GdWCkxBtKWOsKjdch)
   ├─ Video URLs, captions, engagement metrics
   ├─ 10-50 results per target
   └─ ~8-15 seconds per target

   ↓

4️⃣ QUALITY FILTERING (layer1_monitoring/filtering/)
   🔍 Hierarchical Rule Matching
   ├─ Load rules from Lark Base Filter_Rules table
   ├─ Match: strategy+type+value → strategy+type → strategy
   ├─ OR logic: likes≥X OR views≥Y OR engagement_rate≥Z
   ├─ Filter before saving (reduces database noise)
   └─ Metrics: "30 scraped → 16 saved (46.7% filtered out)"

   ↓

5️⃣ SAVE TO LARK BASE (shared/storage/)
   💾 TikTok_Content table
   ├─ Only filtered content saved (deduplication by content_id)
   ├─ Lark lookup auto-populates monitoring_strategy from Target
   └─ Fields: video_url, caption, likes, views, etc.

   ↓

6️⃣ AI ANALYSIS & UPDATE (layer2_analysis/)
   🤖 Strategy-Aware Analysis Routing
   ├─ Read saved content WITH monitoring_strategy
   ├─ Route to strategy-specific prompts:
   │  ├─ Competitor Intelligence → Product/marketing insights
   │  ├─ Niche Deep-Dive → Content strategy analysis
   │  └─ Trend Discovery → (prompt TBD)
   ├─ Video + subtitle analysis (Gemini 2.5 Flash)
   └─ Update Lark records with AI analysis
```

### Key Design Patterns

- **Modular Processors**: BaseProcessor → ProfileProcessor, HashtagProcessor (extensible)
- **Strategy Routing**: Different analysis prompts for different monitoring strategies
- **Hierarchical Filtering**: 3-level rule matching (most specific to fallback)
- **Fail-Open Safety**: No matching rule? Save all content (prevents data loss)
- **Configuration-Driven**: Targets and rules managed in Lark Base (non-technical team access)

---

## 🎯 Monitoring Strategies

AIbrary supports **three monitoring strategies**, each with different goals and AI analysis approaches:

### 1. Competitor Intelligence ✅
**Goal**: Monitor direct competitors to understand their product/marketing strategies

**Targets**:
- Profiles: @blinkist, @headway (competitor apps)
- Focus: Product features, marketing messaging, user engagement tactics

**AI Analysis**:
- Strategic insights for product positioning
- Marketing messaging analysis
- Competitive differentiation opportunities
- Strategic score (0-10) for prioritization

**Volume**: ~30-50 videos per competitor per run
**Use Case**: "What are competitors doing that we're not?"

---

### 2. Niche Deep-Dive ✅
**Goal**: Learn from adjacent niches to discover transferable content strategies

**Targets**:
- Profiles: @notionhq, @characterai, @elsaspeak (adjacent niche tools)
- Hashtags: #book, #productivity, #podcasts, #learning (niche topics)

**AI Analysis**:
- Content strategy insights (hooks, formats, storytelling)
- niche_category classification (7 categories: Books & Reading, Podcasts, etc.)
- Engagement tactics and community-building patterns
- Transferable strategies to AI/ML education

**Volume**: ~30-50 items per target per run
**Use Case**: "What content strategies work in adjacent niches?"

---

### 3. Trend Discovery 🚧
**Goal**: Identify viral AI/ML content and emerging narratives (infrastructure ready)

**Planned Targets**:
- Hashtags: #ai, #machinelearning, #gpt, #chatgpt
- Search: "ChatGPT-4 launch", "OpenAI Sora", etc.

**AI Analysis** (prompt TBD):
- Viral signal detection (why is this trending?)
- Narrative identification (what story is resonating?)
- Trend velocity (accelerating or fading?)

**Planned Volume**: ~100+ items → filter to top 10% most viral
**Use Case**: "What's going viral in AI/ML right now?"

---

## 🔍 Quality Filtering System

**Problem**: Scraping 100+ items per run floods database with low-quality content (spam, low engagement, outdated posts)

**Solution**: Filter content **before saving** to Lark Base using configurable quality rules

### How It Works

1. **Load Rules from Lark Base** (`Filter_Rules` table)
   - Each rule specifies: `monitoring_strategy`, `target_type`, `target_value` (optional)
   - Thresholds: `min_likes`, `min_views`, `min_engagement_rate`, `max_age_days`

2. **Hierarchical Rule Matching** (most specific wins)
   - Level 3: strategy + type + value (e.g., "Competitor Intelligence + profile + @blinkist")
   - Level 2: strategy + type (e.g., "Niche Deep-Dive + hashtag")
   - Level 1: strategy only (fallback)

3. **OR Logic Filtering**
   - Content passes if **ANY** threshold is met (not all)
   - Example: `likes≥1000 OR views≥10000 OR engagement_rate≥2.5%`
   - If ANY condition passes → save to database

4. **Fail-Open Design**
   - No matching rule? Save all content (prevents data loss from misconfig)
   - Warning logged for targets without rules

### Current Production Results

**Real-world test** (Feature 006):
- **Scraped**: 30 items from @elsaspeak
- **Saved**: 16 items (passed quality thresholds)
- **Filtered out**: 14 items (46.7% filter rate)
- **Rule matched**: "Niche Deep-Dive + profile" → `likes≥1000 OR views≥10000`

### Example Rules

| Strategy | Type | Thresholds | Use Case |
|----------|------|------------|----------|
| Competitor Intelligence | profile | likes≥300 OR views≥10,000 | Competitor product posts |
| Niche Deep-Dive | hashtag | likes≥3,000 OR views≥50,000 | High-quality niche content |
| Niche Deep-Dive | profile | likes≥1,000 OR views≥10,000 | Expert creator content |

**For detailed filtering guide**, see [FILTERING_RULES_GUIDE.md](FILTERING_RULES_GUIDE.md)

---

## 📁 Project Structure (Three-Layer Architecture)

```
AIbrary/
├── .specify/                    # SpecKit specification framework
│   ├── memory/                  # Project context and principles
│   ├── specs/                   # Feature specifications
│   │   ├── 000-lark-foundation/ # Foundation spec
│   │   ├── 001-tiktok-monitoring/ # TikTok monitoring spec
│   │   └── 002-two-stage-ai/   # Two-stage AI analysis spec
│   └── progress/                # Development tracking
│
├── src/                         # Three-layer architecture
│   ├── shared/                  # Shared modules (core + storage)
│   │   ├── core/               # Data models and config
│   │   │   ├── models.py       # MonitoringTarget, TikTokContent, FilterRule
│   │   │   └── config.py       # Environment configuration
│   │   └── storage/            # Data persistence
│   │       └── lark_client.py  # Lark Base integration
│   │
│   ├── layer1_monitoring/       # Layer 1: Scraping + Filtering
│   │   ├── scraping/           # Content acquisition
│   │   │   ├── profile_processor.py # Profile scraping (@username)
│   │   │   ├── hashtag_processor.py # Hashtag scraping (#hashtag)
│   │   │   ├── search_processor.py  # Search scraping (keywords)
│   │   │   └── factory.py      # Processor routing
│   │   ├── filtering/          # Quality filtering (Feature 006)
│   │   │   ├── rule_matcher.py # Hierarchical rule matching
│   │   │   └── content_filter.py # OR logic filtering + metrics
│   │   └── orchestrator.py     # Layer 1 orchestration
│   │
│   ├── layer2_analysis/         # Layer 2: AI Analysis
│   │   ├── video_analyzer.py   # Strategy-aware analysis routing
│   │   ├── prompts.py          # Strategy-specific prompts
│   │   └── parsers.py          # Response parsing
│   │
│   ├── layer3_aigc/             # Layer 3: AIGC Generation (planned)
│   │   └── (to be implemented) # Sora cameo, podcast, etc.
│   │
│   └── run_monitoring.py        # Main entry point (Layers 1+2)
│
├── config/                      # Configuration
│   └── .env                    # Environment variables (gitignored)
│
├── ARCHITECTURE.md             # System architecture design
├── CHANGELOG.md                # Version history
├── FILTERING_RULES_GUIDE.md   # Quality filtering documentation
│
└── docs/                        # Documentation
    ├── setup/                  # Setup guides
    ├── logs/                   # Output logs
    └── archive/                # Historical docs
```

---

## 🔧 Current Status

### ✅ Features 001-006 Complete + Architecture Reorganization

**Three-Layer Architecture** (2025-11-08):
- ✅ **Layer 1 (Monitoring)**: `layer1_monitoring/` - Scraping + Filtering
- ✅ **Layer 2 (Analysis)**: `layer2_analysis/` - AI-powered analysis
- ✅ **Layer 3 (AIGC)**: `layer3_aigc/` - Skeleton ready for content generation
- ✅ **Shared Modules**: `shared/` - Core models + storage
- ✅ All imports updated, pipeline tested and working

**Multi-Strategy Monitoring** (Features 003-005):
- ✅ Profile monitoring: @blinkist, @headway, @notionhq, @elsaspeak
- ✅ Hashtag monitoring: #book, #productivity, #podcasts, #learning
- ✅ Strategy-aware analysis routing (Competitor Intelligence, Niche Deep-Dive)
- ✅ 3 monitoring strategies supported (Trend Discovery infrastructure ready)

**Quality Filtering System** (Feature 006):
- ✅ Pre-save filtering with hierarchical rule matching
- ✅ OR logic thresholds (likes, views, engagement_rate, age)
- ✅ 46.7% filter rate in production (30 scraped → 16 saved)
- ✅ Rules managed in Lark Base Filter_Rules table

**AI Analysis** (Features 002-005):
- ✅ Video + subtitle analysis with Gemini 2.5 Flash
- ✅ Strategy-specific prompts (COMPETITOR_INTEL, NICHE_DEEPDIVE)
- ✅ Niche category classification (7 categories)
- ✅ Content strategy insights (hooks, formats, engagement tactics)
- ✅ Strategic scoring (0-10) with proper differentiation

**Data Pipeline**:
- ✅ 6-step pipeline: load → route → scrape → filter → save → analyze
- ✅ No duplicate records (Phase 5 update logic)
- ✅ Lark Base integration with automatic strategy propagation
- ✅ 28 records analyzed in production database

**Cost Performance**:
- ✅ ~$5.50/month actual costs (vs $11-25 budget)
- ✅ Quality filtering reduces database noise (saves storage)
- ✅ Well under $50/month target

### 🚧 Next Phase

**Phase 5: Trend Discovery AI Prompt** (infrastructure ready):
- Implement TREND_DISCOVERY_PROMPT for viral content analysis
- Add SearchProcessor for keyword monitoring
- Test with #ai, #machinelearning, #gpt hashtags
- Viral signal detection and trend velocity analysis

**Future Enhancements**:
- Multi-platform expansion (Instagram, LinkedIn, YouTube Shorts)
- Team collaboration workflows
- Real-time alerts and notifications
- Analytics dashboard and reporting

---

## 💰 Cost Optimization

### Current Costs (Multi-Strategy System with Filtering)

| Service | Usage | Monthly Cost | Notes |
|---------|-------|--------------|-------|
| **Apify** | Profile + Hashtag scraping | ~$5 | Quality filtering reduces waste |
| **Google Gemini** | AI video analysis | ~$0.50 | Gemini 2.5 Flash (cost-effective) |
| **Lark Base** | Team collaboration | $0 | Free tier sufficient |
| **Total** | | **~$5.50/month** | Well under $50 target |

### Cost Savings from Quality Filtering

**Before Filtering** (hypothetical):
- Scrape 100 items/target/run → Save all 100 → Analyze all 100
- Cost: 100 items × $0.01/analysis = $1.00 per target

**After Filtering** (actual):
- Scrape 100 items → Filter to 50 items → Save 50 → Analyze 50
- Cost: 50 items × $0.01/analysis = $0.50 per target
- **50% cost reduction** on AI analysis + storage

**Real Production Example**:
- @elsaspeak: 30 scraped → 16 saved (46.7% filtered)
- AI cost: 16 analyses instead of 30 (**46.7% savings**)
- Storage: 16 records instead of 30 (**46.7% less database noise**)

### Projected Costs (3-Strategy Full System)

| Strategy | Targets | Volume/Month | Est. Cost |
|----------|---------|--------------|-----------|
| Competitor Intelligence | 2 profiles | ~100 items | $2-5 |
| Niche Deep-Dive | 3 profiles + 4 hashtags | ~350 items | $5-10 |
| Trend Discovery | 5 hashtags + search | ~500 items (filtered to 50) | $8-15 |
| **Total** | | ~550-600 quality items | **$15-30/month** |

Still well under $50/month budget!

---

## 🛠️ Setup Guide

### 1. Prerequisites

**Required Accounts**:
- **Apify** - TikTok scraping ([console.apify.com](https://console.apify.com))
- **Lark Base** - Team database (Base ID: `Qr40bFHf8aKpBosZjXbcjF4rnXe`)

**System Requirements**:
- Python 3.11+
- pip package manager

### 2. Installation

```bash
# Clone and enter directory
git clone <repository>
cd "AIbrary Monitoring Layer"

# Install Python dependencies
pip install -r requirements.txt

# Set up environment
cp config/.env.example config/.env
```

### 3. Configuration

**Edit `config/.env`**:
```env
# Lark API (pre-configured)
LARK_APP_ID=cli_a860785f5078100d
LARK_APP_SECRET=sfH5BBpCd6tTeqfPB1FRlhV3JQ6M723A
LARK_BASE_ID=Qr40bFHf8aKpBosZjXbcjF4rnXe

# Apify (add your token)
APIFY_TOKEN=your_apify_api_token_here
TIKTOK_ACTOR_ID=GdWCkxBtKWOsKjdch

# Google Gemini (add your API key)
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Add Monitoring Targets

**In Lark Base**, add to `Monitoring_Targets` table:

**Example 1: Competitor Intelligence (Profile)**
| Field | Value | Notes |
|-------|-------|-------|
| target_value | `@blinkist` | TikTok username |
| platform | `tiktok` | Platform |
| target_type | `profile` | Profile monitoring |
| monitoring_strategy | `Competitor Intelligence` | Strategy (required) |
| active | ✅ | Enable monitoring |
| results_limit | `30` | Posts per run |
| team_notes | `Direct competitor - book summaries` | Purpose |

**Example 2: Niche Deep-Dive (Hashtag)**
| Field | Value | Notes |
|-------|-------|-------|
| target_value | `#book` | Hashtag |
| platform | `tiktok` | Platform |
| target_type | `hashtag` | Hashtag monitoring |
| monitoring_strategy | `Niche Deep-Dive` | Strategy (required) |
| active | ✅ | Enable monitoring |
| results_limit | `50` | Posts per run |
| team_notes | `Adjacent niche - book content strategies` | Purpose |

**Example 3: Niche Deep-Dive (Profile)**
| Field | Value | Notes |
|-------|-------|-------|
| target_value | `@notionhq` | TikTok username |
| platform | `tiktok` | Platform |
| target_type | `profile` | Profile monitoring |
| monitoring_strategy | `Niche Deep-Dive` | Strategy (required) |
| active | ✅ | Enable monitoring |
| results_limit | `30` | Posts per run |
| team_notes | `Adjacent tool - productivity content` | Purpose |

### 5. Add Quality Filter Rules (Optional but Recommended)

**In Lark Base**, add to `Filter_Rules` table:

**Example: Niche Deep-Dive Profile Filter**
| Field | Value | Notes |
|-------|-------|-------|
| monitoring_strategy | `Niche Deep-Dive` | Strategy |
| target_type | `profile` | Target type |
| target_value | *(leave blank)* | Applies to all profiles |
| min_likes | `1000` | Minimum likes threshold |
| min_views | `10000` | Minimum views threshold |
| active | ✅ | Enable rule |

This creates an OR filter: content passes if `likes≥1000` OR `views≥10000`

**For more details**, see [FILTERING_RULES_GUIDE.md](FILTERING_RULES_GUIDE.md)

### 6. Run Monitor

```bash
python3 src/run_monitoring.py
```

**Expected Output**:
```
🚀 Starting TikTok monitoring run...
📋 Loading active targets from Lark...
   Found 3 active targets
[1/3] Processing @blinkist (Competitor Intelligence)...
✅ Scraped 30 items → Filtered to 25 items (16.7% filtered out)
💾 Saved 25 new items to Lark Base
🤖 Analyzing 25 Competitor Intelligence items...
✅ Analysis complete!
```

---

## 📊 Output Data

### Scraped Content Fields

Each TikTok video includes:
- **content_id**: Unique TikTok video ID
- **video_url**: Direct link to TikTok video
- **author_username**: Content creator
- **caption**: Video description/caption
- **likes, comments, views**: Engagement metrics
- **engagement_rate**: Calculated (likes+comments)/views
- **team_status**: new/reviewed/approved/ignored
- **discovered_date**: When content was found

### Example Output (docs/logs/scraper_output_log.json)

```json
{
  "scraping_session": {
    "target": "@openai",
    "results_found": 10,
    "processing_time": "8.6s",
    "status": "success"
  },
  "extracted_content": [
    {
      "content_id": "7555943311534460174",
      "video_url": "https://www.tiktok.com/@openai/video/7555943311534460174",
      "author_username": "openai",
      "caption": "...",
      "engagement_rate": 0.0
    }
  ]
}
```

---

## 🔮 Future Roadmap

### ✅ Completed Phases

**Phase 1-4**: Foundation, AI Analysis, Strategy Routing, Quality Filtering
- ✅ Profile + Hashtag monitoring
- ✅ Multi-strategy system (Competitor Intelligence, Niche Deep-Dive)
- ✅ AI analysis with strategy-specific prompts
- ✅ Quality filtering system

### Phase 5: Trend Discovery AI Prompt
- **Implementation**: TREND_DISCOVERY_PROMPT for viral content analysis
- **Targets**: #ai, #machinelearning, #gpt, #chatgpt (infrastructure ready)
- **SearchProcessor**: Keyword-based monitoring ("ChatGPT-4 launch", etc.)
- **Benefits**: Early detection of viral trends and emerging narratives

### Phase 6+: Advanced Features
- **Multi-Platform Expansion**:
  - Instagram: Reels and Stories
  - LinkedIn: Professional AI content
  - YouTube Shorts: Video content analysis
- **Team Collaboration**:
  - Real-time alerts and notifications
  - Shared tagging and curation workflows
  - Team dashboards and reporting
- **Analytics & Insights**:
  - Trend velocity tracking
  - Competitive positioning maps
  - Content performance analytics

---

## 🐛 Troubleshooting

### Common Issues

**"APIFY_TOKEN not found"**:
- Add your Apify API token to `config/.env`

**"No active targets found"**:
- Add @openai target to Lark `Monitoring_Targets` table
- Ensure `active` field is checked

**"UserFieldConvFail" errors**:
- Lark table field types need adjustment
- Use clean tables or fix field configurations

### Getting Help

- Check [setup guide](docs/setup/manual-setup-guide.md)
- Review [SpecKit specifications](.specify/specs/)
- See [project constitution](.specify/memory/constitution.md)

---

## 👥 Development

### SpecKit Workflow

1. **Specification First**: All features start with `.specify/specs/`
2. **Implementation**: Follow spec requirements exactly
3. **Testing**: Validate against success criteria
4. **Documentation**: Update structure and progress

### Adding New Processors

```python
# src/layer1_monitoring/scraping/new_processor.py
from .base import BaseProcessor

class NewProcessor(BaseProcessor):
    def can_process(self, target):
        return target.target_type == "new_type"

    def process(self, target):
        # Implementation here
        pass
```

Processor automatically registered via `ProcessorFactory`.

---

## 📚 Resources

- **Architecture Design**: [ARCHITECTURE.md](ARCHITECTURE.md) - Three-layer system design
- **Filtering Guide**: [FILTERING_RULES_GUIDE.md](FILTERING_RULES_GUIDE.md) - Quality filtering setup
- **SpecKit Framework**: [.specify/](.specify/)
- **Lark Open Platform**: [open.larksuite.com](https://open.larksuite.com)
- **Apify Documentation**: [docs.apify.com](https://docs.apify.com)
- **Project Specifications**: [.specify/specs/](.specify/specs/)

---

**Developer**: Leo Wu | **AI Assistant**: Claude (Anthropic)
**Last Updated**: 2025-11-08 | **Version**: 5.0 (Three-Layer Architecture)