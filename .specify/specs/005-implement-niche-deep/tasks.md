# Tasks: Niche Deep-Dive Monitoring Strategy

**Input**: Design documents from `/specs/005-implement-niche-deep/`
**Prerequisites**: plan.md ✅, spec.md ✅

**Tests**: Manual validation with real TikTok data (no formal test framework)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/` at repository root
- Python 3.11+ with modular architecture

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Ensure Lark Base schema and code model support niche_category field

- [ ] T001 [Setup] Verify niche_category column exists in Lark Base TikTok Content table (Single Select with 7 options: Podcasts & Audio Learning, Books & Reading, Productivity & Habits, AI in Education, Upskilling & Career, Knowledge Management, Other)
- [ ] T002 [P] [Setup] Add niche_category field to TikTokContent model in `src/core/models.py` (if not already present)
- [ ] T003 [P] [Setup] Update LarkClient field mapping to read/write niche_category in `src/storage/lark_client.py`

**Checkpoint**: Lark Base schema and code models support niche_category field

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement HashtagProcessor - required by both US1 and US2

**⚠️ CRITICAL**: US2 (Niche Hashtag Monitoring) depends on this being complete

- [ ] T004 [Foundation] Create `src/scraping/hashtag_processor.py` file
- [ ] T005 [Foundation] Implement HashtagProcessor class extending BaseProcessor in `src/scraping/hashtag_processor.py`
  - Implement `can_process()` method to check `target.is_hashtag and target.platform == "tiktok"`
  - Implement `_prepare_apify_input()` method with hashtag configuration
  - Reuse `_process_dataset_items()` from ProfileProcessor pattern
- [ ] T006 [Foundation] Export HashtagProcessor in `src/scraping/__init__.py`
- [ ] T007 [Foundation] Verify ProcessorFactory automatically picks up HashtagProcessor (no changes needed - factory uses duck typing)

**Checkpoint**: HashtagProcessor ready - can scrape hashtag targets

---

## Phase 3: User Story 1 - Adjacent Niche Creator Monitoring (Priority: P1) 🎯 MVP

**Goal**: Monitor adjacent niche profiles (@notionhq, @characterai, @elsaspeak) using existing ProfileProcessor

**Independent Test**: Add @notionhq as Niche Deep-Dive target, run monitor.py, verify ProfileProcessor handles it and content saves to Lark (no AI analysis yet - that's US4)

### Implementation for User Story 1

- [ ] T008 [US1] Add adjacent niche profile targets to Lark Base Monitoring Targets table
  - target_value: @notionhq, @characterai, @elsaspeak
  - target_type: profile
  - monitoring_strategy: Niche Deep-Dive
  - active: true
  - results_limit: 50
- [ ] T009 [US1] Run `python3 src/monitor.py` to test ProfileProcessor with Niche Deep-Dive targets
- [ ] T010 [US1] Verify content scraped and saved to Lark with monitoring_strategy="Niche Deep-Dive"
- [ ] T011 [US1] Verify content skipped for analysis (gracefully skipped with "Niche Deep-Dive - skipping (prompt not implemented)" message)

**Checkpoint**: US1 COMPLETE - ProfileProcessor successfully handles adjacent niche profiles, content saved to Lark, gracefully skips analysis (analysis implemented in US4)

---

## Phase 4: User Story 2 - Niche Hashtag Monitoring (Priority: P2)

**Goal**: Monitor niche hashtags (#AIed, #upskill, #habits) using HashtagProcessor

**Independent Test**: Add #AIed as Niche Deep-Dive target, run monitor.py, verify HashtagProcessor scrapes 50-100 items and saves to Lark

### Implementation for User Story 2

- [ ] T012 [US2] Test HashtagProcessor with single hashtag target
  - Add target to Lark: target_value="#AIed", target_type="hashtag", monitoring_strategy="Niche Deep-Dive", active=true, results_limit=100
  - Run `python3 src/monitor.py`
  - Verify 50-100 items scraped
  - Verify content saved to Lark with monitoring_strategy="Niche Deep-Dive"
- [ ] T013 [US2] Add additional niche hashtag targets to Lark
  - #upskill, #habits, and book/podcast-related hashtags
  - Verify each target scrapes successfully
- [ ] T014 [US2] Verify filtering to 30-50 items works (check scraped count vs saved count)

**Checkpoint**: US2 COMPLETE - HashtagProcessor successfully scrapes niche hashtags, filters quality content, saves to Lark

---

## Phase 5: User Story 3 - Quality-First Filtering for Niche Relevance (Priority: P3)

**Goal**: Apply quality filtering that prioritizes niche relevance over raw engagement

**Independent Test**: Compare engagement-only vs quality filtering on same dataset, verify niche-relevant content ranks higher

### Implementation for User Story 3

**NOTE**: Quality filtering logic should be implemented in HashtagProcessor._process_dataset_items() - this is a refinement of US2

- [ ] T015 [US3] Review current filtering logic in HashtagProcessor (likely just taking all items)
- [ ] T016 [US3] Implement quality scoring in HashtagProcessor
  - Add `_calculate_quality_score()` method to HashtagProcessor
  - Formula: quality_score = f(niche_keywords, content_length, engagement_rate)
  - Niche keywords: count occurrences of "podcast", "book", "reading", "productivity", "learning", "upskill", "habit" in subtitles
- [ ] T017 [US3] Implement top-30-50 filtering in HashtagProcessor
  - Sort by quality_score descending
  - Take top 30-50 items (or all if fewer than 30)
- [ ] T018 [US3] Test quality filtering with real hashtag data
  - Run with #books or #productivity
  - Verify high-engagement but off-topic content filtered out
  - Verify niche-relevant content retained

**Checkpoint**: US3 COMPLETE - Quality filtering prioritizes niche relevance, retains 30-50 best items

---

## Phase 6: User Story 4 - Niche Category Classification and Content Strategy Analysis (Priority: P3)

**Goal**: AI analysis assigns niche_category and identifies content strategies

**Independent Test**: Run analysis on Niche Deep-Dive content, verify niche_category assigned, strategic insights identify content strategies

### Implementation for User Story 4

- [ ] T019 [P] [US4] Create NICHE_DEEPDIVE_PROMPT in `src/analysis/prompts.py`
  - Focus on niche_category classification (7 options)
  - Focus on content strategies (hook types, format styles)
  - Focus on topic trends
  - Request 2-3 actionable insights for AIbrary
  - Follow same structure as COMPETITOR_INTELLIGENCE_PROMPT
- [ ] T020 [P] [US4] Implement `_analyze_niche_deepdive()` method in `src/analysis/video_analyzer.py`
  - Format prompt with content data
  - Call Gemini API
  - Parse response to extract niche_category, strategic_score, strategic_insights
  - Return ContentAnalysis object
- [ ] T021 [US4] Update strategy routing in `video_analyzer.py analyze_content()` method
  - Replace "skipping (prompt not implemented)" with call to `_analyze_niche_deepdive()`
  - Handle niche_category assignment
- [ ] T022 [US4] Update `parsers.py` if needed to parse niche_category from AI response
- [ ] T023 [US4] Run end-to-end test with Niche Deep-Dive targets
  - Scrape from @notionhq or #AIed
  - Verify AI analysis runs
  - Verify niche_category populated in Lark
  - Verify strategic_insights contain content strategy observations
- [ ] T024 [US4] Validate niche_category classification accuracy
  - Review 5-10 analyzed videos
  - Verify niche_category matches content
  - Adjust prompt if needed

**Checkpoint**: US4 COMPLETE - AI analysis assigns niche_category and identifies content strategies, all fields populate correctly in Lark

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validation, documentation, and cleanup

- [ ] T025 [Polish] Run complete monitoring cycle with all 3 strategies (Competitor Intelligence, Trend Discovery mock, Niche Deep-Dive)
  - Verify no conflicts between strategies
  - Verify each strategy routes to correct analysis
  - Verify niche_category only populates for Niche Deep-Dive content
- [ ] T026 [Polish] Update README.md with Niche Deep-Dive examples
  - How to add niche profile targets
  - How to add niche hashtag targets
  - Example niche_category grid view usage
- [ ] T027 [Polish] Create example Lark grid view configurations
  - Niche Deep-Dive view showing niche_category, strategic_score, strategic_insights
  - Filters by niche_category
- [ ] T028 [Polish] Update `.specify/progress/tracking.md` with Feature 005 completion status

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS US2
- **User Story 1 (Phase 3)**: Depends on Setup - can start immediately (ProfileProcessor exists)
- **User Story 2 (Phase 4)**: Depends on Foundational - needs HashtagProcessor
- **User Story 3 (Phase 5)**: Depends on US2 - refines HashtagProcessor filtering
- **User Story 4 (Phase 6)**: Depends on US1 or US2 having content - implements AI analysis
- **Polish (Phase 7)**: Depends on US4 completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup (Phase 1) - ProfileProcessor already exists ✅
- **User Story 2 (P2)**: Depends on Foundational (Phase 2) - HashtagProcessor implementation
- **User Story 3 (P3)**: Depends on US2 - enhances HashtagProcessor
- **User Story 4 (P3)**: Depends on US1 OR US2 - needs content to analyze

### Within Each User Story

- Setup tasks before implementation
- Scraping before analysis
- Test after each increment
- Validate before moving to next story

### Parallel Opportunities

- T002 and T003 can run in parallel (different files)
- T019 and T020 can run in parallel (different files)
- US1 and Phase 2 (Foundation) can run in parallel (US1 doesn't need HashtagProcessor)

---

## Parallel Example: User Story 4 Implementation

```bash
# Launch prompt and analyzer method together:
Task: "Create NICHE_DEEPDIVE_PROMPT in src/analysis/prompts.py"
Task: "Implement _analyze_niche_deepdive() method in src/analysis/video_analyzer.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003) - 10 minutes
2. Complete Phase 3: User Story 1 (T008-T011) - 15 minutes
3. **STOP and VALIDATE**: ProfileProcessor handles niche profiles
4. Result: Can monitor @notionhq, @characterai, @elsaspeak (no AI analysis yet)

### Full Feature Delivery

1. Complete Setup (Phase 1) → Foundation ready
2. Complete Foundational (Phase 2) → HashtagProcessor ready
3. Add User Story 1 → Profile monitoring works ✅
4. Add User Story 2 → Hashtag monitoring works ✅
5. Add User Story 3 → Quality filtering works ✅
6. Add User Story 4 → AI analysis works ✅
7. Polish → Complete feature validated

### Incremental Testing Points

After each phase, test independently:
- **After US1**: `python3 src/monitor.py` with @notionhq target
- **After US2**: `python3 src/monitor.py` with #AIed target
- **After US3**: Verify 30-50 items filtered from 100+
- **After US4**: Check Lark for niche_category values

---

## Notes

- [P] tasks = different files, can run in parallel
- [Story] label maps task to specific user story
- ProfileProcessor reuse is key to US1 speed
- HashtagProcessor pattern follows ProfileProcessor
- Quality filtering built into processor, not separate step
- AI analysis is final step (US4) - everything else works without it
- Manual testing with real data (no unit tests)
- Commit after each user story checkpoint
- User requested incremental steps with approval - follow task order strictly
