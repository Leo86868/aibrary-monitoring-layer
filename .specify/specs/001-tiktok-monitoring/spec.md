# Feature Specification: TikTok Content Monitoring

**Feature Branch**: `001-tiktok-monitoring`
**Created**: 2025-10-18
**Status**: Active Implementation
**Dependencies**: 000-lark-foundation (Lark tables and API setup)

## Overview

This specification covers the TikTok-specific implementation details for the AIbrary monitoring system. The foundation (Lark tables, API connections) is covered in `000-lark-foundation`.

## Strategic Monitoring Types

### 1. Competitor Intelligence (Profile-based)
- **Target**: Specific creators (@openai, @nvidia, @anthropic)
- **Volume**: 20 posts per run
- **Focus**: Creator performance, content strategy, audience engagement

### 2. Trend Discovery (Hashtag-based + Hot News)
- **Target**: Trending hashtags (#ai, #machinelearning, #gpt) + breaking news keywords
- **Volume**: 100+ posts per run, filter to top 10%
- **Focus**: Viral content identification, emerging narratives, breaking AI news

### 3. Niche Deep-Dive (Specialized Communities)
- **Target**: Long-tail hashtags (#airesearch, #mlops, #aiethics)
- **Volume**: 30-50 posts per run
- **Focus**: Expert insights, technical discussions, specialized content

## Implementation Files

### Core Documents
- **Database Design**: `comprehensive-database-v1.md` - Complete table schemas
- **Implementation Tasks**: `tasks.md` - Step-by-step implementation plan
- **Field Review**: `table-fields-review.md` - Field-by-field analysis

### Dependencies
- **Foundation**: `../000-lark-foundation/` - Lark setup and API configuration
- **Credentials**: App ID `cli_a860785f5078100d`, Base `Qr40bFHf8aKpBosZjXbcjF4rnXe`

## Monitoring Strategy Classification

Content is classified by monitoring strategy to enable strategy-specific analysis and filtering:

**Strategy Types:**
- **Competitor Intelligence**: Profile-based tracking of specific companies (@openai, @blinkist_app, @headway.app)
- **Trend Discovery**: Hashtag/viral content identification (future)
- **Niche Deep-Dive**: Specialized community tracking (future)

**Implementation:**
- `monitoring_strategy` field added to Monitoring Targets table (Single Select)
- Propagates to TikTok Content table via Lookup field through Target link
- Lookup condition: `target_value is Target` (follows link relationship)

**Current Focus:** Competitor Intelligence strategy is fully implemented with tailored AI analysis prompts (see Feature 002).

## Current Status

**Status**: Competitor Intelligence strategy complete and operational.

**Next Steps**: Implement Trend Discovery and Niche Deep-Dive strategies when needed.

## Key Features

- Multi-strategy monitoring (competitor, trends, niche)
- Rich metadata collection (engagement, creator authority, content analysis)
- Team collaboration features (flags, notes, assignments)
- Strategic value scoring (competitive intel, trend signals)
- Scalable filtering and processing rules
- Strategy-based content classification

**See `comprehensive-database-v1.md` for complete technical specifications.**