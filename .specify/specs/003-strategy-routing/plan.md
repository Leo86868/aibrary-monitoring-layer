# Implementation Plan: Strategy-Aware Analysis Routing

**Feature**: 003-strategy-routing
**Created**: 2025-10-20
**Status**: Planning

## Overview

Implement strategy-aware routing for AI analysis to gracefully skip non-competitor content and enable future multi-strategy prompts.

## Tech Stack

**Existing Stack** (no new dependencies):
- Python 3.x
- Google Gemini API (google-generativeai)
- Lark Base API (requests)
- Existing project structure

**No New Libraries Required** - This feature extends existing VideoAnalyzer class

## Architecture

### Current State
```
VideoAnalyzer.analyze_content()
  ├─ analysis_type parameter (manual, defaults to "competitor_intelligence")
  ├─ _analyze_competitor_intelligence() - uses COMPETITOR_INTELLIGENCE_PROMPT
  └─ _analyze_general() - legacy method
```

### Target State
```
VideoAnalyzer.analyze_content()
  ├─ Read content.monitoring_strategy (from Lark Base lookup)
  ├─ Route based on strategy value:
  │   ├─ "Competitor Intelligence" → _analyze_competitor_intelligence()
  │   ├─ "Trend Discovery" → skip with message (future implementation)
  │   ├─ "Niche Deep-Dive" → skip with message (future implementation)
  │   └─ None/Unknown → skip with warning
  └─ batch_analyze() reports summary by strategy
```

## Project Structure

```
src/
├── core/
│   └── models.py                    # [MODIFY] Add monitoring_strategy field to TikTokContent
├── analysis/
│   ├── video_analyzer.py            # [MODIFY] Add routing logic to analyze_content()
│   └── prompts.py                   # [NO CHANGE] COMPETITOR_INTELLIGENCE_PROMPT already exists
└── storage/
    └── lark_client.py               # [NO CHANGE] monitoring_strategy auto-populated via lookup
```

## Key Design Decisions

### 1. Field Reading Strategy
- **Decision**: Read `monitoring_strategy` from `TikTokContent.monitoring_strategy` field
- **Rationale**: Field is already populated via Lark Base lookup, no API changes needed
- **Implementation**: Add field to dataclass with `Optional[str] = None` default

### 2. Routing Logic Location
- **Decision**: Implement routing in `VideoAnalyzer.analyze_content()` method
- **Rationale**: Central point of control, easy to extend with new strategies
- **Implementation**: Replace hardcoded `analysis_type` parameter with `content.monitoring_strategy` check

### 3. Graceful Skipping
- **Decision**: Return `None` from `analyze_content()` for unimplemented strategies with informative logging
- **Rationale**: Maintains backward compatibility, prevents errors, provides visibility
- **Implementation**: Log skip message, return None (existing code already handles None gracefully)

### 4. Future Extensibility
- **Decision**: Use dictionary-based routing (future enhancement)
- **Rationale**: Easy to add new strategies without modifying core logic
- **Current**: if/elif chain (simple, 3 strategies only)
- **Future**: `STRATEGY_PROMPTS = {"Competitor Intelligence": _analyze_competitor, ...}`

## Implementation Phases

### Phase 1: Data Model Extension
- Add `monitoring_strategy` field to `TikTokContent` dataclass
- No database changes needed (field already exists in Lark via lookup)

### Phase 2: Routing Logic (User Story 1 - P1)
- Modify `analyze_content()` to read `content.monitoring_strategy`
- Add routing logic for three strategy values
- Implement graceful skipping with logging

### Phase 3: Batch Analysis Enhancement (User Story 2 - P1)
- Track analyzed vs skipped counts by strategy
- Generate summary report after batch processing
- Update logging to show strategy for each item

### Phase 4: Testing & Validation
- Test with mixed-strategy content
- Verify Competitor Intelligence still works
- Verify Trend Discovery and Niche Deep-Dive skip gracefully
- Verify summary metrics are accurate

## Success Metrics

- ✅ All Competitor Intelligence content analyzed successfully
- ✅ Trend Discovery and Niche Deep-Dive content skipped without errors
- ✅ Accurate summary reporting (analyzed vs skipped by strategy)
- ✅ Backward compatibility maintained (existing code still works)
- ✅ Easy to extend (adding new strategy requires only 2 changes)

## Dependencies

- Feature 001: TikTok Monitoring (monitoring_strategy field exists)
- Feature 002: Two-Stage AI Analysis (COMPETITOR_INTELLIGENCE_PROMPT works)

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| monitoring_strategy field not populated | Add None check, log warning, skip analysis |
| Unknown strategy values | Treat as "not implemented", log warning, skip |
| Breaking existing code | Maintain backward compatibility, add monitoring_strategy as optional field |
| Performance impact | None expected - just reading one field and adding if/elif logic |

## Timeline Estimate

- Phase 1: 15 minutes (data model)
- Phase 2: 30 minutes (routing logic)
- Phase 3: 20 minutes (batch analysis)
- Phase 4: 20 minutes (testing)
- **Total**: ~1.5 hours

## Future Enhancements

1. **Dictionary-based routing** for cleaner extensibility
2. **Strategy-specific prompts** for Trend Discovery and Niche Deep-Dive
3. **Configurable strategy routing** (allow users to enable/disable strategies)
4. **Analytics dashboard** showing content distribution across strategies
