# Quickstart: Pre-Save Quality Filtering System

**Feature**: 006-implement-pre-save
**Updated**: 2025-10-21

## Overview

The Pre-Save Quality Filtering System automatically filters scraped TikTok content based on quality thresholds before saving to Lark Base. This guide walks you through setup, configuration, and testing.

---

## Prerequisites

1. **Lark Base Setup** (Manual - Do First):
   - Create a new table named `Filter_Rules` in your Lark Base
   - Add the following columns:
     - `strategy` (Select: "Competitor Intelligence", "Trend Discovery", "Niche Deep-Dive")
     - `target_type` (Select: "profile", "hashtag", "search")
     - `target_value` (Text, optional)
     - `min_likes` (Number, optional)
     - `min_views` (Number, optional)
     - `min_engagement_rate` (Number, optional)
     - `max_age_days` (Number, optional)
     - `active` (Checkbox, default True)

2. **Code Implementation** (After setup):
   - Feature 006 code merged to main branch
   - `src/filtering/` module exists
   - `monitor.py` updated with filtering integration

---

## Setup Steps

### Step 1: Create Sample Filter Rules

Add these test rules to your `Filter_Rules` table in Lark Base:

**Rule 1: Competitor Intelligence - Profile (General)**
- strategy: `Competitor Intelligence`
- target_type: `profile`
- target_value: _(leave empty)_
- min_likes: `5000`
- min_views: `10000`
- active: 

**Rule 2: Competitor Intelligence - @blinkist (VIP Target)**
- strategy: `Competitor Intelligence`
- target_type: `profile`
- target_value: `@blinkist`
- min_likes: `1000`
- min_views: `5000`
- active: 

**Rule 3: Niche Deep-Dive - Hashtag**
- strategy: `Niche Deep-Dive`
- target_type: `hashtag`
- target_value: _(leave empty)_
- min_likes: `10000`
- min_views: `50000`
- min_engagement_rate: `2.0`
- active: 

### Step 2: Run the Monitoring Pipeline

```bash
cd "/Users/leowu/AIbrary Monitoring Layer"
python3 src/monitor.py
```

**Expected Output**:
```
<¯ Starting AIbrary TikTok Monitoring System
=Ë Loaded 3 active filter rules

Processing @blinkist (Competitor Intelligence - profile):
   <× Processing profile: @blinkist
    Profile @blinkist: Found 10 videos
   = Filtering with rule: Competitor Intelligence + profile + @blinkist
   10 scraped ’ 8 saved (2 filtered out)
   =¾ Saved 8 items to Lark Base

Processing #book (Niche Deep-Dive - hashtag):
   <÷ Processing hashtag: #book
    Hashtag #book: Found 50 videos
   = Filtering with rule: Niche Deep-Dive + hashtag
   50 scraped ’ 12 saved (38 filtered out)
   =¾ Saved 12 items to Lark Base

 Pipeline complete!
```

### Step 3: Verify Results

1. **Check Lark Base TikTok_Content table**:
   - Count total records added (should match "saved" counts)
   - Verify all saved content meets threshold requirements
   - Example: For @blinkist, all saved content should have likes >= 1000 OR views >= 5000

2. **Check filtering logs** (if issues):
   - Look for "Filtering with rule: ..." messages
   - Verify correct rule was matched (most specific)
   - Check "X scraped ’ Y saved" counts

---

## Testing Scenarios

### Test 1: Strategy-Level Filtering (User Story 1)

**Goal**: Verify basic filtering works with strategy-level rule

**Setup**:
- Add rule: `("Competitor Intelligence", None, None, min_likes=5000)`
- Target: Any Competitor Intelligence target

**Expected Result**:
- Only content with likes >= 5000 is saved
- Content with <5000 likes is filtered out
- Metrics show correct filtered count

**Validation**:
```bash
# Run pipeline
python3 src/monitor.py

# Check output
# Should see: "X scraped ’ Y saved (Z filtered out)"
# Verify Z = count of items with <5000 likes
```

---

### Test 2: Target-Type Specific Filtering (User Story 2)

**Goal**: Verify different rules for profiles vs hashtags

**Setup**:
- Rule 1: `("Niche Deep-Dive", "profile", None, min_likes=5000)`
- Rule 2: `("Niche Deep-Dive", "hashtag", None, min_likes=10000)`
- Targets: One Niche Deep-Dive profile + one hashtag

**Expected Result**:
- Profile content with 6000 likes is saved (meets profile rule)
- Hashtag content with 6000 likes is filtered out (fails hashtag rule)
- Each target uses its type-specific rule

**Validation**:
- Check Lark Base - profile content with 6000 likes should exist
- Hashtag content with 6000 likes should NOT exist
- Logs show correct rule matched for each target type

---

### Test 3: Target-Specific Override (User Story 3)

**Goal**: Verify @blinkist gets special treatment

**Setup**:
- Rule 1: `("Competitor Intelligence", "profile", "@blinkist", min_likes=1000)`
- Rule 2: `("Competitor Intelligence", "profile", None, min_likes=5000)`
- Targets: @blinkist + another profile (e.g., @audiobooks)

**Expected Result**:
- @blinkist content with 2000 likes is saved (meets target-specific rule)
- @audiobooks content with 2000 likes is filtered out (fails general rule)
- Hierarchical matching selects most specific rule

**Validation**:
- Check logs for "Filtering with rule: ... + @blinkist" for @blinkist target
- Check logs for "Filtering with rule: ... + profile" for @audiobooks target
- Verify @blinkist content with 2000 likes exists in Lark Base
- Verify @audiobooks content with 2000 likes does NOT exist

---

### Test 4: Fail-Open Behavior

**Goal**: Verify system saves all content when filtering fails

**Setup**:
- Temporarily make Filter_Rules table inaccessible (rename it)
- Run pipeline

**Expected Result**:
- Pipeline continues without crashing
- Warning logged: "Failed to load filter rules, saving all content"
- All scraped content is saved (0 filtered out)

**Validation**:
```bash
# Rename table in Lark Base to "Filter_Rules_BACKUP"
# Run pipeline
python3 src/monitor.py

# Should see: "  Failed to load filter rules, saving all content"
# Should see: "X scraped ’ X saved (0 filtered out)"
# Restore table name when done
```

---

## Configuration Examples

### Example 1: Aggressive Filtering for Trend Discovery

**Use Case**: Only want highly viral content from trending hashtags

**Rule Configuration**:
```
strategy: Trend Discovery
target_type: hashtag
min_likes: 20000
min_views: 100000
min_engagement_rate: 5.0
max_age_days: 7
```

**Effect**: Only saves content that is:
- Recent (< 7 days old) AND
- Highly viral (20K+ likes OR 100K+ views OR 5%+ engagement)

### Example 2: Relaxed Filtering for VIP Competitor

**Use Case**: Capture all @blinkist content regardless of engagement

**Rule Configuration**:
```
strategy: Competitor Intelligence
target_type: profile
target_value: @blinkist
min_likes: 0
min_views: 0
```

**Effect**: Saves all @blinkist content (thresholds set to 0 = always pass)

### Example 3: Engagement-Only Filter

**Use Case**: Filter by engagement rate only, ignore raw metrics

**Rule Configuration**:
```
strategy: Niche Deep-Dive
target_type: profile
min_engagement_rate: 3.0
```

**Effect**: Saves content with >=3% engagement rate (likes/views), ignores absolute numbers

---

## Troubleshooting

### Issue 1: No Filtering Applied (All Content Saved)

**Symptoms**:
- Metrics show "X scraped ’ X saved (0 filtered out)"
- Expected some content to be filtered

**Possible Causes**:
1. No matching rule exists for target's strategy/type
2. All rules have `active=False`
3. Filter_Rules table doesn't exist or is empty
4. Thresholds set too low (0 = everything passes)

**Solutions**:
- Check rule matching: Verify strategy and target_type match exactly
- Verify active=True in Lark Base
- Add appropriate rule for the target
- Increase threshold values

---

### Issue 2: Too Much Content Filtered (Nothing Saved)

**Symptoms**:
- Metrics show "X scraped ’ 0 saved (X filtered out)"
- Expected some content to pass

**Possible Causes**:
1. Thresholds set too high
2. AND logic mistakenly expected (feature uses OR logic)
3. Content genuinely has low engagement

**Solutions**:
- Lower threshold values gradually
- Remember: Content passes if ANY threshold is met (not all)
- Check scraped content metrics in logs
- Consider target-specific rule with lower thresholds

---

### Issue 3: Wrong Rule Being Applied

**Symptoms**:
- Logs show unexpected rule matched
- Example: Target-specific rule not used, falling back to type-level

**Possible Causes**:
1. target_value mismatch (case-sensitive: @Blinkist ` @blinkist)
2. Empty string vs None confusion
3. Multiple rules at same specificity level

**Solutions**:
- Check target_value exact match (including @ symbol)
- Verify target_type is set correctly
- Delete duplicate rules at same specificity level

---

## Advanced Usage

### Dynamic Rule Adjustment

**Scenario**: You notice hashtag filtering is too aggressive after first run

**Process**:
1. Open Lark Base Filter_Rules table
2. Find hashtag rule (e.g., "Niche Deep-Dive + hashtag")
3. Lower min_likes from 10000 to 5000
4. Save changes
5. Run pipeline again - new threshold takes effect immediately

**No code deployment needed!**

---

### Disabling Filtering Temporarily

**Scenario**: You want to scrape everything for one run

**Process**:
1. Open Lark Base Filter_Rules table
2. Uncheck `active` checkbox for all rules
3. Run pipeline - all content saved (fail-open)
4. Re-check `active` to restore filtering

**Alternative**: Delete all rules from table (pipeline will fail-open)

---

### Strategy-Specific Tuning

**Scenario**: Different strategies need different quality bars

**Configuration**:
```
Rule 1 (Competitor Intelligence - strict):
  strategy: Competitor Intelligence
  min_likes: 5000
  min_views: 10000

Rule 2 (Niche Deep-Dive - relaxed):
  strategy: Niche Deep-Dive
  min_likes: 1000
  min_views: 5000

Rule 3 (Trend Discovery - very strict):
  strategy: Trend Discovery
  min_likes: 20000
  min_views: 100000
  max_age_days: 7
```

Each strategy filters independently based on its rule!

---

## Next Steps

After verifying filtering works:

1. **Tune Rules**: Adjust thresholds based on observed content quality
2. **Add VIP Rules**: Create target-specific rules for high-priority competitors
3. **Monitor Metrics**: Track filtered/saved ratios over time
4. **Iterate**: Refine rules as you learn what content is valuable

**Remember**: Filtering is adaptive - change rules in Lark Base anytime without code changes!
