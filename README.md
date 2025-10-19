# AIbrary - TikTok Monitoring System

A scalable, specification-driven TikTok monitoring system for competitor intelligence. Built with Python, Lark Base integration, and Apify scraping - designed for cost-effective content analysis under $50/month.

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
# Edit config/.env with your Apify token

# Run the processor
python3 run_processor.py
```

## 🎯 What is AIbrary?

A **working TikTok competitor intelligence system** that automatically:
- ✅ **Scrapes @openai TikTok profile** (10 videos in 8.6s)
- ✅ **Scalable processor architecture** for profiles, hashtags, search
- ✅ **Lark Base integration** for team collaboration
- ✅ **Cost-optimized** processing under $50/month
- ✅ **SpecKit compliant** specification-driven development

---

## 🏗️ Architecture

### Current Implementation (Working)

```
📥 LARK INPUT
  └─ Monitoring_Targets table
     → @openai (active, results_limit: 10)

     ↓

⚡ PYTHON PROCESSOR
  ├─ ProfileProcessor (@username) ✅ WORKING
  ├─ HashtagProcessor (#hashtag) → Phase 2
  └─ SearchProcessor (keywords) → Phase 3

     ↓

📊 APIFY INTEGRATION
  └─ Synchronous API call → 10 videos in 8.6s

     ↓

📤 LARK OUTPUT
  └─ TikTok_Content table
     → Engagement metrics, URLs, captions
```

### Scalable Foundation

- **BaseProcessor**: Abstract class for all target types
- **ProcessorFactory**: Routes targets to correct processors
- **Modular Design**: Add new platforms by implementing processors
- **Configuration-Driven**: All settings in `config/` directory

---

## 📁 Project Structure (SpecKit Compliant)

```
AIbrary/
├── .specify/                    # SpecKit specification framework
│   ├── memory/                  # Project context and principles
│   ├── specs/                   # Feature specifications
│   └── progress/                # Development tracking
│
├── src/                         # Source code (Python application)
│   ├── processors/              # Target processors
│   │   ├── profile_processor.py # ✅ Profile scraping (implemented)
│   │   ├── hashtag_processor.py # → Hashtag scraping (Phase 2)
│   │   └── search_processor.py  # → Search scraping (Phase 3)
│   ├── models.py               # Data models
│   ├── lark_client.py          # Lark Base integration
│   └── tiktok_processor.py     # Main application
│
├── config/                      # Configuration
│   ├── .env                    # Environment variables
│   └── *.json                 # Structured configuration
│
├── scripts/                     # Utility scripts
│   ├── node/                   # Lark setup scripts
│   └── python/                 # Python utilities
│
├── docs/                        # Documentation
│   ├── setup/                  # Setup guides
│   ├── logs/                   # Output logs
│   └── archive/                # Historical docs
│
└── run_processor.py            # Main entry point
```

---

## 🔧 Current Status

### ✅ Working Features

**TikTok Profile Monitoring**:
- ✅ Scrapes @openai profile successfully
- ✅ Extracts 10 videos in 8.6 seconds
- ✅ Processes engagement metrics (likes, comments, views)
- ✅ Saves to Lark Base (field type issues being resolved)
- ✅ Clean error handling and logging

**Architecture**:
- ✅ Scalable processor factory pattern
- ✅ SpecKit compliant development workflow
- ✅ Clean project structure
- ✅ Configuration-driven behavior

### 🔄 Next Phase

**Phase 2 - Hashtag Monitoring**:
- Implement `HashtagProcessor.process()`
- Add #ai, #artificialintelligence targets
- Test hashtag scraping performance

**Phase 3 - Search Monitoring**:
- Implement `SearchProcessor.process()`
- Add keyword-based monitoring
- Regional trend analysis

---

## 💰 Cost Optimization

### Current Costs (Profile Monitoring)

| Service | Usage | Monthly Cost |
|---------|-------|--------------|
| **Apify** | ~1000 profiles/month | $5-10 |
| **Lark Base** | Team collaboration | $0-12 |
| **Total** | | **$5-22/month** |

### Planned Optimizations
- Smart result limits based on target importance
- Duplicate content detection
- Rate limiting for cost control
- Batch processing efficiency

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
```

### 4. Add Monitoring Targets

**In Lark Base**, add to `Monitoring_Targets` table:

| Field | Value | Notes |
|-------|-------|-------|
| target_value | `@openai` | TikTok username |
| platform | `tiktok` | Platform |
| target_type | `profile` | Type |
| active | ✅ | Enable monitoring |
| results_limit | `10` | Posts per run |
| team_notes | `Competitor intelligence` | Purpose |

### 5. Run Processor

```bash
python3 run_processor.py
```

**Expected Output**:
```
🚀 Starting TikTok monitoring run...
📋 Loading active targets from Lark...
   Found 1 active targets
[1/1] Processing: @openai
🎯 Processing profile: @openai
✅ Profile @openai: Found 10 videos in 8.6s
🎉 Processing complete!
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

### Phase 2: Hashtag Monitoring
- **Targets**: #ai, #artificialintelligence, #machinelearning
- **Implementation**: HashtagProcessor class
- **Benefits**: Discover trending topics and viral content

### Phase 3: Search Monitoring
- **Targets**: "artificial intelligence", "AI trends"
- **Implementation**: SearchProcessor class
- **Benefits**: Keyword-based content discovery

### Phase 4: Multi-Platform
- **Instagram**: Reels and Stories
- **LinkedIn**: Professional AI content
- **YouTube Shorts**: Video content analysis

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
# src/processors/new_processor.py
from processors.base import BaseProcessor

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

- **SpecKit Framework**: [.specify/](.specify/)
- **Lark Open Platform**: [open.larksuite.com](https://open.larksuite.com)
- **Apify Documentation**: [docs.apify.com](https://docs.apify.com)
- **Project Specifications**: [.specify/specs/](.specify/specs/)

---

**Developer**: Leo Wu | **AI Assistant**: Claude (Anthropic)
**Last Updated**: 2025-10-18 | **Version**: 3.0 (Python + SpecKit)