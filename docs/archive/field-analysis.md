# Field Analysis: Essential vs Over-Engineering

## Current Reality Check

You're building a **TikTok monitoring system** to:
1. Track competitors like @openai
2. Discover trending AI content
3. Find high-value posts for team review

**Key Question**: What data do you actually need to make decisions?

---

## Essential Fields Analysis

### Monitoring_Targets - Keep Only:
- `target_value` (@openai, #ai, etc.) - **ESSENTIAL**
- `platform` (tiktok) - **ESSENTIAL**
- `target_type` (profile/hashtag) - **ESSENTIAL**
- `active` (on/off) - **ESSENTIAL**
- `results_limit` (how many posts) - **ESSENTIAL**
- `team_notes` (why monitoring this) - **USEFUL**

### TikTok_Content - Keep Only:
- `content_id` (TikTok video ID) - **ESSENTIAL**
- `target_id` (link to monitoring target) - **ESSENTIAL**
- `video_url` (link to TikTok) - **ESSENTIAL**
- `author_username` (@openai) - **ESSENTIAL**
- `caption` (the text) - **ESSENTIAL**
- `likes`, `comments`, `views` - **ESSENTIAL** (for filtering)
- `engagement_rate` (calculated) - **ESSENTIAL** (for filtering)
- `team_notes` (team's assessment) - **USEFUL**
- `team_status` (new/reviewed/approved) - **USEFUL**
- `discovered_date` (when found) - **ESSENTIAL**

---

## Over-Engineering Red Flags

### Probably Unnecessary:
- `author_authority_score` - Who calculates this? How?
- `virality_score` - Complex calculation, may not be useful
- `technical_depth` - Subjective, hard to automate
- `strategic_value_score` - Over-complex scoring
- `competitive_intel_value` - Redundant with team notes
- `trend_signal_strength` - Can be derived from engagement
- `transcription_confidence` - Implementation detail
- `effects_used`, `sounds_used` - Nice-to-have, not essential
- `video_thumbnail_url` - TikTok provides this anyway
- `review_deadline`, `assigned_analyst` - Premature optimization

### Definitely Unnecessary:
- `author_bio` - Available on TikTok
- `author_display_name` - Available on TikTok
- `author_follower_count` - Changes frequently, available on TikTok
- `posting_timestamp` - Available from TikTok
- `processed_timestamp` - Implementation detail
- `video_duration` - Available from TikTok

### Complex Tables That May Be Overkill:
- `Content_Processing_Rules` table - Could start with simple config file instead

---

## Simplified Proposal

### Monitoring_Targets (8 fields)
```
- target_value (text) - "@openai"
- platform (select) - "tiktok"
- target_type (select) - "profile"/"hashtag"
- active (checkbox)
- results_limit (number) - 20
- team_notes (text)
- created_date (auto)
- last_processed (date)
```

### TikTok_Content (12 fields)
```
- content_id (text) - TikTok video ID
- target_id (link) - Links to monitoring target
- video_url (url)
- author_username (text)
- caption (text)
- likes (number)
- comments (number)
- views (number)
- engagement_rate (number) - Calculated
- team_status (select) - "new"/"reviewed"/"approved"
- team_notes (text)
- discovered_date (date)
```

### Questions for You:

1. **Do you actually need** transcription? (Costs money, adds complexity)
2. **Do you need** AI relevance scoring? (Costs money, team can judge manually)
3. **Do you need** multiple strategies or just start with competitor monitoring?
4. **How will your team actually use this** - what decisions will they make with the data?

**Current tables have 60+ fields. Simplified version has 20 fields.**

Should we strip it down to essentials and build up from there?