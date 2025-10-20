# Implementation Plan: Two-Stage AI Analysis Upgrade

**Branch**: `002-two-stage-ai` | **Date**: 2025-10-19 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `.specify/specs/002-two-stage-ai/spec.md`

## Summary

Upgrade AIbrary's TikTok monitoring system to use content-first relevance scoring through a two-stage AI analysis approach. System will analyze content topics objectively first, then apply strategic competitor intelligence scoring. Single API call optimization reduces costs by 50% while improving accuracy of learning/book content detection regardless of creator identity.

## Technical Context

**Language/Version**: Python 3.11 (existing codebase)
**Primary Dependencies**: google-generativeai 0.8.5, requests, python-dotenv, apify-client
**Storage**: Lark Base API (existing database integration)
**Testing**: Manual testing with real TikTok content and database validation
**Target Platform**: macOS/Linux CLI application
**Project Type**: Single project - enhancement to existing monitoring system
**Performance Goals**: <10 seconds per content analysis including database save, single API call per content item
**Constraints**: <$50/month operational cost (constitution requirement), maintain existing Lark Base schema
**Scale/Scope**: Process 10-50 content items per monitoring run, 4 strategic analysis fields, 1 general analysis field

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Specification-First Development**: Complete specification created with user stories, requirements, and success criteria
✅ **Cost-Conscious Engineering**: 50% cost reduction through single API call optimization, maintains <$50/month target
✅ **Configuration-Driven Architecture**: AIbrary context and prompts externalized, no hardcoded analysis logic
✅ **Test-First Validation**: Success criteria defined with measurable outcomes and test scenarios

**Gate Status**: PASSED - All constitution principles satisfied

## Project Structure

### Documentation (this feature)

```
.specify/specs/002-two-stage-ai/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
src/
├── ai_analysis.py       # MODIFY: Two-stage analysis implementation
├── data.py             # MODIFY: Add update method for existing records
├── core.py             # MODIFY: Update data models if needed
└── monitor.py          # EXISTING: Main monitoring pipeline

config/
└── .env                # EXISTING: API keys and configuration

requirements.txt        # EXISTING: Python dependencies
```

**Structure Decision**: Single project structure maintained. This is an enhancement to existing monitoring system in `src/` directory. No new major components needed - focusing on upgrading existing AI analysis module and database integration.

## Complexity Tracking

*No constitution violations - tracking not required*

| Component | Complexity Level | Justification |
|-----------|-----------------|---------------|
| Two-stage prompt | Medium | Single API call with structured output parsing |
| Content-first scoring | Low | Logic-based relevance assessment |
| Database updates | Low | Existing Lark API integration enhancement |
| Parsing improvements | Low | Regex pattern updates for new format |

## Phase 0: Research Tasks

- [x] Research Gemini 2.5-flash model capabilities for complex prompts
- [x] Validate single API call approach for two-stage analysis
- [x] Confirm AIbrary competitive context and positioning
- [x] Analyze existing parsing patterns and improvement needs

## Phase 1: Design Artifacts

### Data Model Changes
- Enhanced `TikTokContent` class with strategic analysis fields
- Updated `AnalysisResult` class for two-stage output
- Database field mapping validation

### Contracts
- Updated AI analysis service contract
- Database update/create contract
- Parsing service contract for new response format

### Integration Points
- `ai_analysis.py` ↔ Gemini API (single call)
- `ai_analysis.py` ↔ `data.py` (enhanced saving)
- `data.py` ↔ Lark Base (field updates)

## Implementation Strategy

**MVP Scope**: User Story 1 (Content-First Analysis) + User Story 2 (Single API Call)
**Incremental Delivery**: P1 stories first, then P2/P3 enhancements
**Risk Mitigation**: Test with existing OpenAI content to validate scoring accuracy