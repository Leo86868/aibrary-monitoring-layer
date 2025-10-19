# TikTok Monitoring System

Scalable TikTok competitor intelligence system using Lark Base and Apify.

## 🏗️ Architecture

**Scalable Foundation:**
- **BaseProcessor**: Abstract class for all target types
- **ProfileProcessor**: Handles @username targets (implemented)
- **HashtagProcessor**: Handles #hashtag targets (Phase 2)
- **SearchProcessor**: Handles keyword searches (Phase 3)

**Current Capabilities:**
- ✅ **Profile monitoring**: @openai, @anthropic, etc.
- 🔄 **Hashtag monitoring**: Coming in Phase 2
- 🔄 **Search monitoring**: Coming in Phase 3

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your Apify token
```

### 3. Set Up Lark Base
Your Lark base should have:
- **Monitoring_Targets** table with @openai target
- **TikTok_Content** table for results

### 4. Run Processor
```bash
python tiktok_processor.py
```

## 📊 Expected Output

```
🚀 Starting TikTok monitoring run at 2025-10-18 17:30:00
📋 Loading active targets from Lark...
   Found 1 active targets
🔍 Filtering targets by processor availability...
   ✅ Supported: 1
   ⚠️ Unsupported: 0

⚡ Processing 1 targets...

[1/1] Processing: @openai
🎯 Processing profile: @openai
✅ Profile @openai: Found 10 videos in 15.2s

💾 Saving results to Lark...
   📊 Total content found: 10
   🆕 New content: 10
✅ Saved content: 12345678901
✅ Saved content: 12345678902
...
📊 Saved 10/10 content items

==================================================
📊 PROCESSING SUMMARY
==================================================
⏱️ Total time: 18.5s
🎯 Targets processed: 1
✅ Successful: 1
❌ Failed: 0
📱 Content found: 10

✅ Successful targets:
   - @openai: 10 videos (15.2s)

🎉 Processing complete!
```

## 🔧 Configuration

**Required Environment Variables:**
- `APIFY_TOKEN`: Your Apify API token
- `TIKTOK_ACTOR_ID`: Apify TikTok scraper actor ID

**Lark Configuration:**
- Pre-configured for your Lark Base
- Tables: Monitoring_Targets, TikTok_Content

## 🎯 Adding New Targets

Add targets manually in Lark Base:
- **target_value**: @username
- **platform**: tiktok
- **target_type**: profile
- **active**: ✅ checked
- **results_limit**: 10-50
- **team_notes**: Why monitoring this target

## 📈 Future Expansion

**Phase 2 - Hashtags:**
- Implement HashtagProcessor
- Add #ai, #artificialintelligence targets

**Phase 3 - Search:**
- Implement SearchProcessor
- Add keyword-based monitoring

**Clean expansion** - just implement new processor classes, no architecture changes needed!

## 🏃‍♂️ Running in Production

**Manual runs:**
```bash
python tiktok_processor.py
```

**Automated scheduling:**
```bash
# Add to crontab for daily runs
0 9 * * * cd /path/to/project && python tiktok_processor.py
```

## 🛠️ Troubleshooting

**Common Issues:**
1. **Missing APIFY_TOKEN**: Set in .env file
2. **No active targets**: Add @openai target in Lark Base
3. **Apify actor errors**: Check actor ID and permissions
4. **Lark API errors**: Verify credentials and table names

**Error Handling:**
- Graceful failure per target
- Detailed logging
- Duplicate content detection
- Rate limiting built-in