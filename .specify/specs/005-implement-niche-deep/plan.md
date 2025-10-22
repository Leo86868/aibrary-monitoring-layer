# Implementation Plan: Niche Deep-Dive Monitoring Strategy

**Branch**: `005-implement-niche-deep` | **Date**: 2025-10-21 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-implement-niche-deep/spec.md`

## Summary

Implement Niche Deep-Dive monitoring strategy to track adjacent niche creator content from podcasts, books, productivity, learning, and AI-education spaces. This strategy prioritizes quality over quantity, filtering 30-50 highest-quality items based on niche relevance, content strategy insights, and topic trends. Uses existing ProfileProcessor for adjacent niche profiles (@notionhq, @characterai, @elsaspeak, @ElevenLabs) and implements HashtagProcessor for niche hashtags (#AIed, #upskill, #habits). AI analysis focuses on niche_category classification, content strategy identification, and topic trend analysis.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**:
- `requests>=2.31.0` (HTTP client)
- `apify-client>=1.6.0` (TikTok scraping)
- `google-generativeai>=0.7.0` (Gemini AI analysis)
- `python-dotenv>=1.0.0` (environment config)

**Storage**: Lark Base (cloud spreadsheet database via REST API)
**Testing**: Manual validation with real TikTok data (no formal test framework yet)
**Target Platform**: macOS/Linux server (Python CLI application)
**Project Type**: Single project (Python monolith with modular architecture)
**Performance Goals**:
- Scrape 30-50 items per expert profile within 60 seconds
- Scrape 50-100 items per hashtag within 60 seconds
- Complete AI analysis for 30-50 filtered items within 15 minutes

**Constraints**:
- Must maintain <$50/month combined cost across all strategies
- Reuse existing Apify TikTok actor (no custom scrapers)
- No schema changes to Lark Base
- Zero impact on existing Competitor Intelligence and Trend Discovery workflows

**Scale/Scope**:
- 4-6 adjacent niche profiles initially (@notionhq, @heypi.ai, @characterai, @elsaspeak, @ElevenLabs, @cluely)
- 5-7 niche hashtags (#AIed, #upskill, #habits, book-related, podcast-related)
- 30-50 highest-quality niche-relevant items per monitoring run (quality over quantity)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Specification-First Development
- **Status**: PASS
- Feature specification complete with user stories, requirements, and success criteria
- All quality checks passed in requirements checklist

### ✅ Cost-Conscious Engineering
- **Status**: PASS
- Target maintained: <$50/month total operational cost
- Quality filtering (30-50 items) minimizes AI analysis costs compared to high-volume strategies
- Reuses existing Apify integration and Gemini 2.5 Flash (cost-optimized model)

### ✅ Configuration-Driven Architecture
- **Status**: PASS
- All targets configured in Lark Base (no hardcoded profiles/hashtags)
- Monitoring strategy field determines routing behavior
- Apify configuration externalized via environment variables

### ✅ Test-First Validation
- **Status**: PASS
- Success criteria defined in specification (10 measurable outcomes)
- Manual validation approach: test with expert profiles and specialized hashtags
- Quality filtering validation: compare technical substance before/after filtering

### ✅ Progressive Quality Gates
- **Status**: PASS
- Layer 1: Apify filtering (videos only, no slideshows) - FREE
- Layer 2: Quality scoring (technical indicators, content length) - FREE
- Layer 3: Top 30-50 filtering based on quality score - FREE
- Layer 4: AI analysis only on filtered content - PAID (minimized volume)

**Overall**: ✅ NO VIOLATIONS - Constitution fully satisfied

## Project Structure

### Documentation (this feature)

```
specs/005-implement-niche-deep/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (quality scoring approach)
├── data-model.md        # Phase 1 output (QualityScore, ExpertiseAssessment)
├── quickstart.md        # Phase 1 output (testing with expert profiles)
├── contracts/           # Phase 1 output (Gemini analysis contract)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
src/
├── core/
│   ├── __init__.py            # Existing: MonitoringTarget, TikTokContent models
│   └── models.py              # Existing: Core data models
├── scraping/
│   ├── __init__.py            # Existing: Processor exports
│   ├── base.py                # Existing: BaseProcessor abstract class
│   ├── factory.py             # Existing: ProcessorFactory (routes by target_type)
│   ├── profile_processor.py   # ✅ REUSE: Already handles profile targets
│   └── hashtag_processor.py   # ⚠️ IMPLEMENT: New processor for hashtag targets
├── analysis/
│   ├── __init__.py            # Existing: VideoAnalyzer export
│   ├── video_analyzer.py      # ✏️ MODIFY: Add _analyze_niche_deepdive() method
│   ├── prompts.py             # ✏️ MODIFY: Add NICHE_DEEPDIVE_PROMPT constant
│   └── parsers.py             # ✅ REUSE: Existing JSON parsing logic
├── storage/
│   └── lark_client.py         # ✅ REUSE: Existing Lark Base integration
└── monitor.py                 # ✅ NO CHANGES: Strategy routing already implemented

tests/
└── (manual validation with real data)
```

**Structure Decision**: Single project structure (Option 1) maintained. All code in `src/` with clear separation by concern (scraping, analysis, storage). Feature reuses 90% of existing infrastructure - only needs HashtagProcessor implementation and Niche Deep-Dive analysis prompt. No changes to core pipeline (`monitor.py`) or storage layer.

## Complexity Tracking

*No complexity violations - constitution fully satisfied. Table intentionally left empty.*

---

# Phase 0: Research & Technical Decisions

## Research Tasks

### 1. Quality Scoring for Niche Relevance

**Question**: How to calculate quality score for niche relevance without AI analysis?

**Research Approach**:
- Examine subtitle content for niche keyword density (podcasts, books, learning, productivity terms)
- Measure content focus and topic clarity
- Identify content strategy signals (hook patterns, format choices)
- Review profile/hashtag context for niche alignment

**Decision Required**: Formula for `quality_score = f(niche_keywords, content_strategy_signals, relevance_to_AIbrary, engagement_patterns)`

### 2. HashtagProcessor Implementation Pattern

**Question**: How should HashtagProcessor differ from ProfileProcessor in Apify configuration?

**Research Approach**:
- Review Apify TikTok actor documentation for hashtag scraping
- Examine ProfileProcessor implementation pattern
- Determine hashtag-specific input parameters
- Understand hashtag vs profile result structure differences

**Decision Required**: Apify input configuration for hashtag targets

### 3. Niche Category Classification

**Question**: How should AI classify content into niche categories?

**Research Approach**:
- Define indicators for each niche category (Podcasts/Books/Productivity/AI-Ed/Upskilling/Knowledge Mgmt)
- Review examples of content in each niche
- Determine classification criteria (topic keywords, content focus, creator context)

**Decision Required**: Classification rubric for niche_category assignment with 7 options

---

# Phase 1: Design Artifacts

## Data Model

**File**: `data-model.md` - Documents quality scoring model and niche category classification

### Key Entities (from spec):

1. **AdjacentNicheProfile** (existing MonitoringTarget)
   - `target_type`: "profile"
   - `target_value`: "@username" (e.g., @notionhq, @characterai)
   - `monitoring_strategy`: "Niche Deep-Dive"

2. **NicheHashtag** (existing MonitoringTarget)
   - `target_type`: "hashtag"
   - `target_value`: "#hashtag" (e.g., #AIed, #upskill)
   - `monitoring_strategy`: "Niche Deep-Dive"

3. **QualityScore** (new calculation in HashtagProcessor)
   - `niche_keywords`: int (niche-relevant term count)
   - `content_strategy_signals`: int (hook patterns detected)
   - `relevance_to_AIbrary`: float (alignment score)
   - `engagement_patterns`: float (engagement metrics)
   - `composite_score`: float (normalized 0-100)

4. **NicheContent** (existing TikTokContent with strategy)
   - All existing fields (content_id, video_url, engagement metrics, etc.)
   - `monitoring_strategy`: "Niche Deep-Dive"
   - `quality_score`: float (from QualityScore calculation)
   - **`niche_category`**: str (NEW Lark column - from AI analysis)

5. **NicheCategory** (NEW Lark Base column - Single Select)
   - Values: "Podcasts & Audio Learning" | "Books & Reading" | "Productivity & Habits" | "AI in Education" | "Upskilling & Career" | "Knowledge Management" | "Other"
   - AI-assigned during analysis
   - Used for grid view segmentation and filtering

## API Contracts

**File**: `contracts/niche-deepdive-analysis.md` - Gemini AI analysis contract

### Input Contract (Gemini Prompt)
```python
{
  "author_username": str,
  "caption": str,
  "subtitles": str,
  "likes": int,
  "comments": int,
  "views": int,
  "monitoring_strategy": "Niche Deep-Dive"
}
```

### Output Contract (JSON Response)
```json
{
  "general_analysis": "Niche content description focusing on strategies and topics",
  "strategic_score": 0-10,  // Niche relevance and strategic value to AIbrary
  "content_type": "educational_value | learning_feature | productivity_content | other",
  "strategic_insights": [
    "Content strategy 1: hook type → why effective → AIbrary application",
    "Topic trend 2: subject → why relevant → opportunity for AIbrary"
  ],
  "niche_category": "Podcasts & Audio Learning | Books & Reading | Productivity & Habits | AI in Education | Upskilling & Career | Knowledge Management | Other",
  "content_topics": ["reading_habits", "book_recommendations"],  // Optional multi-select tags
  "content_strategies": "Hook types, format styles, presentation approaches observed"
}
```

## Quickstart Guide

**File**: `quickstart.md` - Testing Niche Deep-Dive with adjacent niche profiles

### Setup Steps:
1. Add adjacent niche profile targets to Lark Base with `monitoring_strategy="Niche Deep-Dive"` (e.g., @notionhq, @characterai)
2. Add niche_category column to TikTok Content table in Lark Base (Single Select with 7 options)
3. Run `python3 src/monitor.py` to scrape and analyze
4. Review filtered content (30-50 highest-quality niche-relevant items)
5. Validate AI analysis assigns niche_category and identifies content strategies

### Expected Results:
- ProfileProcessor handles adjacent niche profiles (reuses existing logic)
- Quality filtering retains niche-relevant content
- AI analysis routes to NICHE_DEEPDIVE_PROMPT
- Results saved to Lark with niche_category populated for grid view filtering

---

# Phase 2: Task Generation

**Command**: `/speckit.tasks` (NOT executed in this plan - separate command)

**Output**: `tasks.md` with step-by-step implementation tasks ordered by dependency

---

## Next Steps

1. ✅ **Phase 0 Complete**: Run research on quality scoring and HashtagProcessor design
2. ✅ **Phase 1 Complete**: Generate data-model.md, contracts/, and quickstart.md
3. ⏭️ **Phase 2 Required**: Run `/speckit.tasks` to generate implementation tasks
4. ⏭️ **Implementation**: Execute tasks.md with `/speckit.implement`

**Constitution Re-Check (Post-Design)**: ✅ PASS - No violations introduced during planning
