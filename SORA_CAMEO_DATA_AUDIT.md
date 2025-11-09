# Sora 2 Character Cameo - Data Audit & Mapping

**Date**: 2025-11-08
**Purpose**: Map existing TikTok monitoring data to Sora 2 character cameo video automation workflow

---

## 1. Current Data Inventory

### Lark Base Tables (4 total)
1. **TikTok_Content** - Main scraped content (28 records)
2. **Monitoring_Targets** - Targets being monitored (6 active)
3. **Filter_Rules** - Quality filtering rules
4. **Update** - Unknown purpose

### TikTok_Content: Available Data

**Total Records**: 28

**Data Completeness**:
- ✅ **28/28** (100%) have `video_download_url`
- ✅ **25/28** (89%) have `strategic_score >= 7` (high quality)
- ✅ **28/28** (100%) have `strategic_insights`
- ⚠️  **21/28** (75%) have `subtitle_url`

**Niche Category Distribution**:
```
N/A: 15 records (54%)  ← PROBLEM: Most content not categorized
Books & Reading: 4
Podcasts & Audio Learning: 2
Productivity & Habits: 2
Upskilling & Career: 2
Other: 2
AI in Education: 1
```

**Monitoring Strategies**:
- `optC7R9ojK`: 15 records (likely "Competitor Intelligence")
- `opt94KPGSJ`: 13 records (likely "Niche Deep-Dive")

**Key Fields Available**:

| Field | Type | Example | Availability | Usable for Sora? |
|-------|------|---------|--------------|------------------|
| `content_id` | Text | `7278031885337398571` | 100% | ❌ Reference only |
| `caption` | Text | `"😮"` or `"Join us at Pemberley..."` | 100% | ✅ **Topic/theme** |
| `strategic_score` | Number | `8` | 100% | ✅ **Quality filter** |
| `strategic_insights` | Long text | See example below | 100% | ✅ **Scene ideas** |
| `niche_category` | Single select | `"Books & Reading"` | 46% | ⚠️  **Character selection** (limited) |
| `engagement_rate` | Number | `0.187499...` | 100% | ✅ **Validation** |
| `video_download_url` | URL | Apify storage link | 100% | ✅ **Visual reference** |
| `subtitle_url` | URL | Apify storage link | 75% | ✅ **Dialogue content** |
| `monitoring_strategy` | Lookup | `opt94KPGSJ` | 100% | ❌ Not directly useful |

### Example `strategic_insights` Content

```
1. **Tactic:** Position AI as an empathetic and decisive advisor for relatable
   personal dilemmas.
   * **Why it works:** This approach humanizes the AI, building an emotional
     connection and trust by addressing common, "messy" human problems with clear,
     supportive guidance.
   * **How AIbrary could test it:** Develop short video content where AIbrary's AI
     provides advice on user-submitted dilemmas related to personal growth,
     decision-making, or managing stress, framed as "AIbrary's Life Lessons" based
     on principles from books in its library.

2. **Tactic:** Use a clear, direct conversational style with simple vocabulary.
   * **Why it works:** Makes the AI accessible and trustworthy...
```

---

## 2. Sora 2 Cameo Workflow Requirements

### Required Inputs (from the workflow spec)

| Input | Required? | Source in Our Data | Availability |
|-------|-----------|-------------------|--------------|
| **Quantity of clips** | Required | Manual config | N/A |
| **Scene description** | Required | ⚠️  Need to generate | Can extract from `strategic_insights` |
| **Cameo usernames** | Required | ❌ **MISSING** | Need to define character library |
| **Reference image** | Optional | `video_download_url` | ✅ 100% |
| **Aspect ratio** | Required | Manual config | N/A |
| **Duration** | Required | Manual config (10 or 15s) | N/A |
| **Quality** | Required | Manual config (Sora 2 or Pro) | N/A |

### Critical Gaps

❌ **Gap 1: No Cameo Character Library**
- We don't have predefined characters/avatars
- Need to create or define character personas

❌ **Gap 2: Scene Descriptions Not Extracted**
- `strategic_insights` contains tactics, not visual scenes
- Need AI agent to convert tactics → scene descriptions

⚠️  **Gap 3: Limited Niche Categories**
- Only 46% of content has `niche_category`
- Hard to auto-select character based on category

---

## 3. Proposed Data Flow: TikTok → Sora 2

### Option A: Use Existing High-Quality Content

**Step 1: Select Source Content**
```python
# Filter high-quality content
source_content = TikTok_Content.filter(
    strategic_score >= 8,  # Very high quality
    video_download_url IS NOT NULL,  # Has visual reference
    subtitle_url IS NOT NULL  # Has dialogue
)
# Result: ~18-20 records available
```

**Step 2: AI Agent Converts Data → Sora Prompts**

INPUT from TikTok_Content:
```json
{
  "content_id": "7278031885337398571",
  "caption": "😮",
  "strategic_insights": "1. Tactic: Position AI as empathetic advisor for personal dilemmas...",
  "video_download_url": "https://api.apify.com/...",
  "subtitle_url": "https://api.apify.com/...",
  "niche_category": "Podcasts & Audio Learning",
  "engagement_rate": 0.187
}
```

AI AGENT PROCESSING (using Gemini/GPT):
```
Prompt to AI:
"Convert this TikTok strategic insight into a Sora 2 video scene description:
- Strategic Insight: {strategic_insights}
- Topic: {caption}
- Style: Inspirational, book-learning related
- Duration: 10 seconds
- Characters needed: 1-2 people discussing/demonstrating the concept

Output format:
{
  'scene_description': '<detailed visual scene>',
  'suggested_characters': ['character_type_1', 'character_type_2'],
  'mood': '<mood/tone>',
  'visual_style': '<art direction>'
}"
```

AI AGENT OUTPUT:
```json
{
  "scene_description": "A cozy modern library with warm lighting. A young woman sits at a round table with an AI assistant hologram across from her. She looks troubled, gesturing as she explains a dilemma. The AI listens empathetically, then offers clear, supportive guidance. Camera slowly pushes in on their conversation.",
  "suggested_characters": ["young_professional_female", "ai_hologram_advisor"],
  "mood": "warm, supportive, intimate",
  "visual_style": "cinematic, soft focus background, golden hour lighting",
  "aspect_ratio": "9:16",
  "duration": 10
}
```

**Step 3: Map to Character Cameos**

PROBLEM: We don't have a character library yet!

SOLUTIONS:
- **Option 1**: Use generic Sora 2 prompts (no cameos) - Just generate scenes based on descriptions
- **Option 2**: Create a small character library first (5-10 characters):
  ```
  - "professional_mentor" (mature, authoritative)
  - "curious_learner" (young, enthusiastic)
  - "wise_narrator" (calm, guiding)
  - "book_lover" (intellectual, warm)
  - "productivity_coach" (energetic, motivating)
  ```
- **Option 3**: Use reference images from `video_download_url` as "character style"

**Step 4: Generate Sora 2 Video**

```python
sora_input = {
    "prompt": scene_description + " " + visual_style,
    "aspect_ratio": "9:16",
    "duration": 10,
    "model": "sora-2",
    "reference_image_url": video_download_url  # Optional: for style matching
}

# Call Sora 2 API via Key.ai
video_result = sora_api.generate(sora_input)
```

---

## 4. Realistic Implementation for TODAY

### What We CAN Do Today

✅ **Step 1**: Create AI agent that converts `strategic_insights` → Sora scene descriptions
✅ **Step 2**: Use high-quality TikTok content (score >= 8) as input source
✅ **Step 3**: Generate Sora 2 videos WITHOUT cameo characters (just scene descriptions)
✅ **Step 4**: Use `video_download_url` as reference images for visual style
✅ **Step 5**: Store generated videos in new Lark Base table

### What We CANNOT Do Today (Missing Data)

❌ **Character cameo integration** - No character library exists
❌ **Niche-based character selection** - Only 46% of content has categories
❌ **Dialogue extraction from subtitles** - Would need to fetch and parse subtitle files

### Recommended MVP for Today

**Focus**: Automated Sora 2 scene generation from TikTok insights (NO cameos yet)

**Workflow**:
1. Select 5 high-quality TikTok records (score >= 8)
2. For each record:
   - Extract scene idea from `strategic_insights`
   - Use AI agent (Gemini) to generate Sora-compatible scene description
   - Optional: Use `video_download_url` as visual style reference
   - Call Sora 2 API to generate 10-second video
   - Save result to new `Generated_Videos` table
3. Review generated videos
4. Decide if cameo characters are needed for v2

**Expected Output**: 5 AI-generated videos inspired by proven TikTok tactics

---

## 5. Data Gaps to Address

### Immediate (for cameo integration)

1. **Create Character Library**
   - Define 5-10 character personas
   - Get Cameo usernames (if using real cameos)
   - OR define AI-generated character styles

2. **Improve Niche Categorization**
   - Re-analyze the 15 records with `niche_category = N/A`
   - Use AI to auto-categorize based on `caption` + `strategic_insights`

3. **Extract Dialogue from Subtitles**
   - Fetch subtitle files from `subtitle_url`
   - Parse and extract key quotes/dialogue
   - Use for character dialogue in videos

### Future (for advanced features)

4. **Add Emotion/Mood Field**
   - Analyze video tone from subtitles
   - Store as metadata for scene generation

5. **Visual Style Tags**
   - Analyze `video_download_url` with Gemini Vision
   - Extract: lighting, color palette, camera angles
   - Store as structured data

---

## 6. Recommended Action Plan for TODAY

### Phase 1: Setup (30 min)
- [ ] Install Sora 2 API dependencies (Key.ai SDK or similar)
- [ ] Test Gemini API for scene description generation
- [ ] Create new Lark Base table: `Sora_Generated_Videos`

### Phase 2: Build AI Agent (2 hours)
- [ ] Create `sora_scene_generator.py`
- [ ] Input: TikTok_Content record
- [ ] Process: Gemini converts `strategic_insights` → scene description
- [ ] Output: Sora-compatible prompt

### Phase 3: Sora Integration (2 hours)
- [ ] Integrate Sora 2 API (via Key.ai)
- [ ] Test with 1 record
- [ ] Batch generate 5 videos
- [ ] Save to Lark Base

### Phase 4: Review & Iterate (1 hour)
- [ ] Review generated videos
- [ ] Assess quality
- [ ] Decide: Add cameo characters? Or continue with pure scene generation?

**Total Time Estimate**: 5-6 hours

---

## 7. Final Recommendation

**For TODAY**: Skip cameo character integration, focus on:
- ✅ AI agent converting TikTok insights → Sora scene descriptions
- ✅ Automated Sora 2 video generation
- ✅ Using existing high-quality data (28 records, 25 with score >= 7)

**For NEXT WEEK**: Add cameo character layer:
- Define character library
- Improve niche categorization
- Add dialogue extraction from subtitles

**Rationale**: We have excellent strategic insights and visual references, but NO character library. Better to validate the core workflow first (TikTok → Sora) before adding character complexity.

---

**Status**: Ready to proceed with simplified workflow (no cameos today)
**Blocker Removed**: Can start implementation immediately
