# Quality Filtering System - Quick Reference Guide

## 📋 Current Rule Coverage Status

### Active Targets (3 total):
| Target | Type | Strategy | Rule Match | Status |
|--------|------|----------|------------|--------|
| `@elsaspeak` | profile | Niche Deep-Dive | Rule 3: Niche Deep-Dive + profile | ✅ COVERED |
| `#book` | hashtag | Niche Deep-Dive | Rule 2: Niche Deep-Dive + hashtag | ✅ COVERED |
| `#endlesslearning` | hashtag | **NOT SET** | None | ⚠️ NOT COVERED |

### Filter Rules (3 total):
| Rule | Strategy | Type | Value | Thresholds |
|------|----------|------|-------|------------|
| 1 | Competitor Intelligence | profile | (blank) | likes≥300 OR views≥10,000 |
| 2 | Niche Deep-Dive | hashtag | (blank) | likes≥3,000 OR views≥50,000 |
| 3 | Niche Deep-Dive | profile | (blank) | likes≥1,000 OR views≥10,000 |

---

## ⚠️ IMPORTANT CAUTIONS

### 🔴 Uncovered Target Warning
**Target `#endlesslearning` has NO `monitoring_strategy` set!**
- This target will **NOT be filtered** - ALL scraped content will be saved
- This can flood your database with low-quality content
- **Action Required:** Set `monitoring_strategy` in Lark Base for this target

### 🟡 Missing Strategy-Level Fallback Rules
**What are fallback rules?**
Strategy-level rules with BOTH `target_type` and `target_value` blank act as fallbacks for targets that don't match type-specific rules.

**Why you might need them:**
- If you add a new target type (e.g., "search" instead of "profile"/"hashtag")
- If you change a target's type and forget to update rules
- As a safety net for unexpected target configurations

**Current Status:**
- ❌ No fallback rule for **Competitor Intelligence**
- ❌ No fallback rule for **Niche Deep-Dive**
- ❌ No fallback rule for **Trend Discovery** (if you use it later)

**Recommendation:** Add strategy-level fallback rules for safety:
```
Rule: Competitor Intelligence (fallback)
  monitoring_strategy: Competitor Intelligence
  target_type: (blank)
  target_value: (blank)
  min_likes: 3000
  min_views: 20000
  active: ✓

Rule: Niche Deep-Dive (fallback)
  monitoring_strategy: Niche Deep-Dive
  target_type: (blank)
  target_value: (blank)
  min_likes: 1000
  min_views: 15000
  active: ✓
```

---

## 🔧 How Filtering Works

### Pipeline Flow:
1. **Scrape** content from TikTok (via Apify)
2. **Check** for duplicates (skip if already in database)
3. **Filter** based on matching rule (quality thresholds)
4. **Save** to Lark Base (only content that passed)

### Hierarchical Rule Matching:
The system tries to find the **most specific** rule that matches:
1. **Level 3 (Most Specific):** strategy + type + value (e.g., "Competitor Intelligence + profile + @blinkist")
2. **Level 2 (Mid-Specific):** strategy + type (e.g., "Niche Deep-Dive + hashtag")
3. **Level 1 (Least Specific):** strategy only (e.g., "Competitor Intelligence")

### OR Logic:
Content passes if it meets **ANY** threshold (not all):
- `likes≥1000` **OR** `views≥10000` **OR** `engagement_rate≥2.5%`
- If ANY one is met, content is saved

### Fail-Open Behavior:
**If NO matching rule is found:**
- System saves ALL content without filtering (fail-open)
- This prevents losing data due to misconfiguration
- **BUT** this can flood your database with low-quality content!

---

## 🎯 Current Filtering Behavior by Target

### `@elsaspeak` (Niche Deep-Dive + profile)
**Rule:** likes≥1,000 OR views≥10,000
- Content with 2,000 likes + 5,000 views: ✅ PASS (likes met)
- Content with 500 likes + 15,000 views: ✅ PASS (views met)
- Content with 500 likes + 5,000 views: ❌ FAIL (neither met)

### `#book` (Niche Deep-Dive + hashtag)
**Rule:** likes≥3,000 OR views≥50,000
- Content with 5,000 likes + 20,000 views: ✅ PASS (likes met)
- Content with 1,000 likes + 60,000 views: ✅ PASS (views met)
- Content with 1,000 likes + 30,000 views: ❌ FAIL (neither met)

### `#endlesslearning` (NO STRATEGY SET)
**Rule:** NONE - No filtering applied!
- Content with 10 likes + 100 views: ✅ PASS (no filter)
- Content with 1,000,000 likes + 10,000,000 views: ✅ PASS (no filter)
- **ALL content is saved without filtering!** ⚠️

---

## 🚀 Recommended Actions

### Immediate (High Priority):
1. **Set `monitoring_strategy` for `#endlesslearning`**
   - Go to Lark Base → Monitoring_Targets table
   - Find `#endlesslearning` row
   - Set `monitoring_strategy` to "Niche Deep-Dive" (or appropriate strategy)

2. **Review Competitor Intelligence threshold**
   - Current: `min_likes=300` is very low (will let in spam)
   - Recommended: `min_likes=2000` or higher

### Optional (Safety Net):
3. **Add strategy-level fallback rules**
   - Protects against future configuration changes
   - Catches unexpected target types
   - See recommendations above

---

## 📊 Testing Your Rules

Run the integration test to see how your rules perform:
```bash
cd "/Users/leowu/AIbrary Monitoring Layer"
python3 /tmp/test_filtering_integration_real.py
```

This shows:
- Which rule matches each target
- Sample content that passes vs fails
- Filter rate (% of content filtered out)
- Recommendations for threshold adjustments

---

## ✅ Quick Checklist

Before running production scraping:
- [ ] All active targets have `monitoring_strategy` set
- [ ] Each strategy has at least one matching rule
- [ ] Thresholds are reasonable (not too strict or permissive)
- [ ] Test filtering with mock data first
- [ ] Consider adding strategy-level fallback rules

**Current Status:**
- [ ] `#endlesslearning` needs `monitoring_strategy` set ⚠️
- [ ] Consider adding fallback rules for safety 🟡
- [x] Filtering logic is working correctly ✅
- [x] Rules cover most active targets (2/3) ✅
