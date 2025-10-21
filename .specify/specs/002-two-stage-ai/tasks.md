# Tasks: Two-Stage AI Analysis Upgrade

**Input**: Design documents from `.specify/specs/002-two-stage-ai/`
**Prerequisites**: plan.md ✅, spec.md ✅
**Branch**: `002-two-stage-ai`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare existing codebase for two-stage AI analysis enhancement

- [x] T001 Validate existing dependencies and API keys in config/.env ✅
- [x] T002 [P] Backup current ai_analysis.py for rollback capability ✅
- [x] T003 [P] Verify new monitoring targets (@openai, @blinkist_app, @headway.app with limit=1) ✅

---

## Phase 2: User Story 1 - Content-First Analysis (Priority P1)

**Goal**: Analyze TikTok content based on topic, not creator identity
**Independent Test**: Content relevance scoring matches topics regardless of creator

- [x] T004 [US1] Update COMPETITOR_INTELLIGENCE_PROMPT in src/analysis/prompts.py with AIbrary context and two-stage structure ✅
- [x] T005 [US1] Modify _analyze_competitor_intelligence() method in src/analysis/video_analyzer.py to implement two-stage analysis in single API call ✅
- [x] T006 [US1] Update _parse_competitor_intelligence_response() in src/analysis/parsers.py to extract both general analysis and strategic fields ✅
- [x] T007 [US1] Fix content_type parsing regex to handle underscores (educational_tips, feature_showcase) ✅
- [x] T008 [US1] Test content-first scoring with real content from @openai ✅
- [x] T009 [US1] Test content-first scoring with real content from @blinkist_app and @headway.app ✅

**Checkpoint**: Content analysis works independently of creator identity ✅

---

## Phase 3: User Story 2 - Cost-Efficient Single API Call (Priority P1)

**Goal**: Perform both analyses in one API call to reduce costs by 50%
**Independent Test**: Single API call populates both general and strategic fields

- [x] T010 [US2] Design two-stage prompt format for single API call in src/analysis/prompts.py ✅
- [x] T011 [US2] Implement parsing logic in src/analysis/parsers.py to extract Stage 1 (general) and Stage 2 (strategic) from single response ✅
- [x] T012 [US2] Update _update_content_with_analysis() in src/analysis/video_analyzer.py to populate both Analysis column and strategic fields ✅
- [x] T013 [US2] Validate API call count monitoring - ensure exactly 1 call per content item ✅
- [ ] T014 [US2] Test database saving with both general analysis and strategic fields populated (DB field missing - blocked)

**Checkpoint**: Single API call provides complete analysis data ✅

---

## Phase 4: User Story 3 - Concise Strategic Insights (Priority P2)

**Goal**: Generate brief, actionable insights with numbered formatting for scannability
**Independent Test**: Insights are concise and contain specific recommendations

- [x] T015 [US3] Redesign strategic insights section of prompt for numbered format (always 1-3 insights) ✅
- [x] T016 [US3] Update parsing logic to extract numbered insights properly ✅
- [x] T017 [US3] Replace redundant relevance_score + strategic_value with single strategic_score (0-10) ✅
- [x] T018 [US3] Define 9 controlled content_type categories for better data grouping ✅
- [x] T019 [US3] Test scoring differentiation - ensure full range 0-10 is utilized ✅
- [x] T020 [US3] Fix AI penalizing based on performance metrics (should focus on strategic value only) ✅
- [x] T021 [US3] Implement isSlideshow filtering in processing.py to skip photo carousels ✅

**Checkpoint**: Strategic insights are numbered, scores differentiated, content types controlled

---

## Phase 5: User Story 4 - Update Existing Records (Priority P3)

**Goal**: Update existing content instead of creating duplicates
**Independent Test**: Re-analysis updates existing record, no duplicates created

- [x] T022 [US4] Add content_exists() method enhancement in src/storage/lark_client.py (returns record_id) ✅
- [x] T023 [US4] Implement update_content() method in src/storage/lark_client.py to modify existing records ✅
- [x] T024 [US4] Modify save_content() in src/storage/lark_client.py to check if content exists before creating ✅
- [x] T025 [US4] Test duplicate prevention by analyzing same content_id twice ✅
- [x] T026 [US4] Validate database contains only one record per content_id after re-analysis ✅

**Checkpoint**: No duplicate records created on re-analysis ✅

---

## Phase 5.5: Video Analysis Enhancement (NEW - Added Today)

**Goal**: Analyze actual video content (not just text) for richer competitive insights
**Motivation**: Video reveals much more than captions - visuals, editing, delivery style

- [x] T027 [NEW] Add video download capability to src/analysis/video_analyzer.py ✅
- [x] T028 [NEW] Integrate Gemini multimodal video analysis API ✅
- [x] T029 [NEW] Update prompts to request visual/editing/delivery insights ✅
- [x] T030 [NEW] Add temporary file cleanup after video analysis ✅
- [x] T031 [NEW] Test video analysis with real OpenAI TikTok videos ✅

**Checkpoint**: AI successfully analyzes video content, not just text ✅

---

## Phase 6: Integration & Validation

**Purpose**: End-to-end testing and performance validation

- [x] T032 [P] End-to-end pipeline test with mock data (Phase 1-4 test scripts) ✅
- [x] T033 [P] Database schema validation - all strategic fields saving correctly ✅
- [x] T034 [P] Fix content_id precision issue (changed to Text field in Lark Base) ✅
- [x] T035 [P] Integration test using monitoring pipeline with real Apify scraping ✅
- [x] T036 [P] Performance test - video analysis takes 60-90s per video (acceptable for quality) ✅
- [x] T037 [P] Prompt refinement - improve analysis output format ✅
- [x] T038 [P] Fix strategic score parser regex bug (was defaulting all scores to 5) ✅

**Checkpoint**: Full end-to-end pipeline validated with real data ✅

**Tools Created**:
- `test_prompt_refinement.py` - Test prompts with real data without modifying production
- `run_analysis_only.py` - Re-analyze existing content without re-scraping

**Key Improvements**:
- **Prompt Quality**: Reduced jargon, added what→why→try structure for insights, focused on marketing tactics
- **Parser Fix**: Corrected regex from `**strategic score**` to `**Score:**` - resolved all-scores-5 bug
- **Score Distribution**: Now seeing real variation (3-9 range) instead of everything defaulting to 5

---

## Dependencies & Parallel Execution

### User Story Dependencies
- **US1 (Content-First)**: Independent - can start immediately
- **US2 (Single API Call)**: Depends on US1 prompt structure
- **US3 (Concise Insights)**: Depends on US2 response format
- **US4 (Update Records)**: Independent - can be developed in parallel

### Parallel Opportunities
- T002, T003 can run in parallel (different concerns)
- T025, T026, T027, T028, T029 can run in parallel (different validation aspects)
- US1 and US4 can be developed simultaneously (different modules)

## Implementation Strategy

**MVP Scope**: User Stories 1 & 2 (P1 priorities)
- Delivers core content-first analysis with cost optimization
- Provides foundation for P2/P3 enhancements

**Incremental Delivery**:
1. Phase 2 (US1) → Content-first analysis working
2. Phase 3 (US2) → Single API call optimization
3. Phase 4 (US3) → Enhanced insight quality
4. Phase 5 (US4) → Database update functionality

**Risk Mitigation**:
- T002 provides rollback capability
- T003 ensures test data available for validation
- Checkpoint testing after each user story phase