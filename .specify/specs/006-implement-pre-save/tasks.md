# Tasks: Pre-Save Quality Filtering System

**Input**: Design documents from `.specify/specs/006-implement-pre-save/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/filtering_api.md, quickstart.md

**Tests**: Tests are NOT requested in the feature specification. This implementation follows manual testing approach per quickstart.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
- Single Python CLI project: `src/` at repository root
- New module: `src/filtering/` for filtering logic
- Existing modules: `src/core/`, `src/storage/`, `src/monitor.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create filtering module structure and prepare for implementation

- [ ] T001 Create `src/filtering/` directory for filtering module
- [ ] T002 Create `src/filtering/__init__.py` with module exports
- [ ] T003 [P] User creates Filter_Rules table in Lark Base with schema (manual step - see quickstart.md)

**Checkpoint**: Filtering module structure ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model that ALL user stories depend on

**  CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Add FilterRule dataclass to `src/core/models.py` with fields: strategy, target_type, target_value, min_likes, min_views, min_engagement_rate, max_age_days, active (frozen=True for immutability)
- [ ] T005 Add FilterRule to `src/core/__init__.py` exports

**Checkpoint**: Foundation ready - FilterRule model available for all user stories

---

## Phase 3: User Story 1 - Strategy-Level Quality Filtering (Priority: P1) <¯ MVP

**Goal**: Implement basic filtering with strategy-level rules. Content is filtered before saving using single strategy-based threshold. This is the foundation of the entire filtering system.

**Independent Test**: Add one strategy-level filter rule in Lark Base ("Competitor Intelligence" with min_likes=5000), run pipeline, verify only content with 5000+ likes is saved. See quickstart.md "Test 1" for detailed steps.

### Implementation for User Story 1

- [ ] T006 [US1] Implement `get_filter_rules()` method in `src/storage/lark_client.py` to fetch active filter rules from Lark Base Filter_Rules table (returns List[FilterRule])
- [ ] T007 [P] [US1] Implement `build_rule_index()` function in `src/filtering/rule_matcher.py` to build composite key dictionary from filter rules (handles strategy-level rules only for now)
- [ ] T008 [P] [US1] Implement `passes_filter()` function in `src/filtering/content_filter.py` to check if content passes filter thresholds using OR logic (checks min_likes, min_views, min_engagement_rate)
- [ ] T009 [US1] Implement `find_matching_rule()` function in `src/filtering/rule_matcher.py` to find strategy-level matching rule (level 1 matching only - tries (strategy, None, None) lookup)
- [ ] T010 [US1] Create FilterMetrics dataclass in `src/filtering/content_filter.py` with fields: total_scraped, filtered_out, saved, rule_used
- [ ] T011 [US1] Implement `filter_content_list()` function in `src/filtering/content_filter.py` to filter list of content and return filtered list + metrics
- [ ] T012 [US1] Add filtering module exports to `src/filtering/__init__.py` (build_rule_index, find_matching_rule, filter_content_list, FilterMetrics)
- [ ] T013 [US1] Integrate filtering into `src/monitor.py`: Load filter rules at pipeline start using get_filter_rules()
- [ ] T014 [US1] Integrate filtering into `src/monitor.py`: Build rule index using build_rule_index() after loading rules
- [ ] T015 [US1] Integrate filtering into `src/monitor.py`: Call filter_content_list() after scraping each target, before saving to Lark Base
- [ ] T016 [US1] Integrate filtering into `src/monitor.py`: Add metrics reporting (print "{total} scraped ’ {saved} saved ({filtered_out} filtered out)")
- [ ] T017 [US1] Add error handling in get_filter_rules() for fail-open behavior (return empty list on Lark API error, log warning)
- [ ] T018 [US1] Add fail-open logic in filter_content_list() when no matching rule found (return all content unfiltered)

**Checkpoint**: At this point, User Story 1 (strategy-level filtering) should be fully functional. Test per quickstart.md "Test 1".

---

## Phase 4: User Story 2 - Target-Type Specific Filtering (Priority: P2)

**Goal**: Add target-type specific rules (profile vs hashtag have different thresholds). Enables more aggressive filtering for hashtags while keeping reasonable thresholds for profiles.

**Independent Test**: Add two rules - "Niche Deep-Dive + profile" (min 5000 likes) and "Niche Deep-Dive + hashtag" (min 10000 likes). Scrape both profile and hashtag, verify each is filtered according to its type-specific rule. See quickstart.md "Test 2".

### Implementation for User Story 2

- [ ] T019 [US2] Update `find_matching_rule()` in `src/filtering/rule_matcher.py` to support level 2 matching (try (strategy, target_type, None) before falling back to level 1)
- [ ] T020 [US2] Update `build_rule_index()` in `src/filtering/rule_matcher.py` to handle target_type normalization (empty string ’ None)
- [ ] T021 [US2] Add logging to `find_matching_rule()` to report which specificity level was matched (DEBUG level)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Test per quickstart.md "Test 2".

---

## Phase 5: User Story 3 - Target-Specific Override Rules (Priority: P3)

**Goal**: Add target-specific rules for VIP targets like @blinkist. Enables special quality thresholds for strategically important competitors.

**Independent Test**: Add target-specific rule for "@blinkist" (min 1000 likes) and general profile rule (min 5000 likes). Scrape @blinkist and another profile, verify @blinkist content with 2000 likes is saved but other profile needs 5000+. See quickstart.md "Test 3".

### Implementation for User Story 3

- [ ] T022 [US3] Update `find_matching_rule()` in `src/filtering/rule_matcher.py` to support level 3 matching (try (strategy, target_type, target_value) first, then fallback to level 2 and level 1)
- [ ] T023 [US3] Update `find_matching_rule()` to use content.target_value for exact matching at level 3 (case-sensitive comparison)
- [ ] T024 [US3] Add hierarchical matching logic documentation in `src/filtering/rule_matcher.py` module docstring

**Checkpoint**: All user stories (1, 2, 3) should now work independently. Test per quickstart.md "Test 3".

---

## Phase 6: User Story 4 - Filtering Metrics and Visibility (Priority: P4)

**Goal**: Add detailed filtering metrics reporting so users can see what was filtered and tune rules.

**Independent Test**: Run pipeline with filtering enabled, verify terminal output shows clear metrics: "X scraped ’ Y saved (Z filtered out)" with correct counts. See quickstart.md "Test scenario 4".

### Implementation for User Story 4

- [ ] T025 [US4] Enhance metrics reporting in `src/monitor.py` to show rule used (e.g., "Filtering with rule: Competitor Intelligence + profile")
- [ ] T026 [US4] Add summary metrics at end of pipeline run showing total scraped, total saved, total filtered across all targets
- [ ] T027 [US4] Add per-strategy metrics breakdown (show filtering stats for each monitoring strategy separately)

**Checkpoint**: All user stories should now be fully functional with comprehensive visibility.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T028 Add engagement_rate calculation in `passes_filter()` if not provided by scraper (formula: likes/views * 100, safe division)
- [ ] T029 Add max_age_days support in `passes_filter()` to filter by content age (calculate age from created_at field)
- [ ] T030 Add comprehensive logging throughout filtering module (DEBUG level for per-item decisions, INFO for summaries)
- [ ] T031 Update CLAUDE.md or project docs with filtering module overview (if project has documentation structure)
- [ ] T032 Run quickstart.md validation - execute all 4 test scenarios end-to-end
- [ ] T033 Run fail-open test from quickstart.md (rename Filter_Rules table, verify pipeline continues)
- [ ] T034 Code cleanup: Remove any debug print statements, ensure consistent code style
- [ ] T035 Final validation: Run full pipeline with Competitor Intelligence and Niche Deep-Dive targets, verify filtering works for both strategies

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after User Story 1 complete (extends find_matching_rule)
  - User Story 3 (P3): Can start after User Story 2 complete (extends find_matching_rule further)
  - User Story 4 (P4): Can start after User Story 3 complete (enhances metrics from US1)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Foundation only - Implements core filtering with strategy-level rules
- **User Story 2 (P2)**: Depends on US1 - Extends hierarchical matching to level 2 (type-specific)
- **User Story 3 (P3)**: Depends on US2 - Extends hierarchical matching to level 3 (target-specific)
- **User Story 4 (P4)**: Depends on US1 - Enhances metrics reporting from basic filtering

**Note**: User Stories 2, 3, 4 are incremental enhancements to User Story 1's core filtering. Each adds capability without breaking previous stories.

### Within Each User Story

- Foundational FilterRule model before any user story
- LarkClient.get_filter_rules() before rule matching logic
- Rule matching before content filtering
- Content filtering before monitor.py integration
- Integration before metrics reporting

### Parallel Opportunities

- **Phase 1 Setup**: T001 and T002 can run in parallel (different files)
- **Phase 2 Foundational**: T004 and T005 are sequential (same file)
- **User Story 1**:
  - T007 (rule_matcher.py) and T008 (content_filter.py) can run in parallel [P]
  - T006 (lark_client.py) independent [P]
  - T009 depends on T007 (same file)
  - T010, T011 are sequential (same file content_filter.py)
  - T013-T018 are sequential (same file monitor.py)
- **User Story 2-4**: Tasks within each story are mostly sequential (same files being extended)
- **Phase 7 Polish**: T028-T030 touch different concerns, some parallelizable
- **User stories themselves CANNOT run in parallel** - each extends the previous implementation

---

## Parallel Example: User Story 1

```bash
# After T005 (Foundational) completes, launch these in parallel:

# Parallel batch 1: Different modules
Task T006: "Implement get_filter_rules() in src/storage/lark_client.py"
Task T007: "Implement build_rule_index() in src/filtering/rule_matcher.py"
Task T008: "Implement passes_filter() in src/filtering/content_filter.py"

# Then sequential:
Task T009: "Implement find_matching_rule() in src/filtering/rule_matcher.py" (depends on T007)
Task T010: "Create FilterMetrics in src/filtering/content_filter.py" (depends on T008)
Task T011: "Implement filter_content_list() in src/filtering/content_filter.py" (depends on T010)
Task T012: "Add exports to src/filtering/__init__.py" (depends on T009, T011)

# Integration (sequential - all in monitor.py):
Task T013: "Load filter rules in src/monitor.py"
Task T014: "Build rule index in src/monitor.py"
Task T015: "Call filter_content_list in src/monitor.py"
Task T016: "Add metrics reporting in src/monitor.py"
Task T017: "Add error handling in get_filter_rules()"
Task T018: "Add fail-open logic in filter_content_list()"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T005) - CRITICAL
3. Complete Phase 3: User Story 1 (T006-T018)
4. **STOP and VALIDATE**: Test User Story 1 independently per quickstart.md Test 1
   - Add strategy-level rule in Lark Base
   - Run pipeline
   - Verify filtering works (only content meeting threshold is saved)
5. If working, you have an MVP! Basic filtering operational.

### Incremental Delivery

1. Complete Setup + Foundational ’ FilterRule model ready
2. Add User Story 1 ’ Test per quickstart.md Test 1 ’ **MVP deployed** (strategy-level filtering)
3. Add User Story 2 ’ Test per quickstart.md Test 2 ’ **Enhancement deployed** (type-specific filtering)
4. Add User Story 3 ’ Test per quickstart.md Test 3 ’ **Enhancement deployed** (target-specific VIP rules)
5. Add User Story 4 ’ Test per quickstart.md Test 4 ’ **Enhancement deployed** (detailed metrics)
6. Each story adds value without breaking previous functionality

### Sequential Team Strategy

With one developer (typical for this project):

1. Complete Setup + Foundational (T001-T005)
2. Complete User Story 1 (T006-T018) ’ Test ’ Deploy MVP
3. Complete User Story 2 (T019-T021) ’ Test ’ Deploy enhancement
4. Complete User Story 3 (T022-T024) ’ Test ’ Deploy enhancement
5. Complete User Story 4 (T025-T027) ’ Test ’ Deploy enhancement
6. Polish (T028-T035) ’ Final validation

**Recommended pause points**: After each user story completion, test independently before proceeding.

---

## Notes

- [P] tasks = different files/modules, can run in parallel
- [Story] label maps task to specific user story (US1, US2, US3, US4)
- Each user story should be independently testable per quickstart.md
- No automated tests - manual testing approach per quickstart.md
- Fail-open philosophy: Prefer saving content over losing data on errors
- User Story 1 is the critical MVP - must work before proceeding
- User Stories 2-4 are incremental enhancements, not blocking
- Stop after any user story to validate, tune rules, and deploy
- FilterRule model (T004) is critical foundation - blocks everything else

---

## Task Summary

**Total Tasks**: 35
- Phase 1 (Setup): 3 tasks
- Phase 2 (Foundational): 2 tasks
- Phase 3 (User Story 1 - MVP): 13 tasks
- Phase 4 (User Story 2): 3 tasks
- Phase 5 (User Story 3): 3 tasks
- Phase 6 (User Story 4): 3 tasks
- Phase 7 (Polish): 8 tasks

**Parallel Opportunities**: 6 tasks marked [P] (different files/modules)

**Independent Test Criteria**:
- User Story 1: Strategy-level filtering works (quickstart.md Test 1)
- User Story 2: Type-specific filtering works (quickstart.md Test 2)
- User Story 3: Target-specific VIP rules work (quickstart.md Test 3)
- User Story 4: Detailed metrics displayed (quickstart.md Test 4)

**Suggested MVP Scope**: User Story 1 only (T001-T018) = 18 tasks total for working filtering system
