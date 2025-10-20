# Changelog

All notable changes to the AIbrary TikTok Monitoring System.

## [Unreleased] - 2025-01-20

### Added - Video Analysis Feature
- **Multimodal Video Analysis**: AI now analyzes actual video content, not just text
  - Downloads videos temporarily for analysis
  - Uses Gemini 2.5 Flash multimodal capabilities
  - Analyzes visual presentation, editing style, on-screen text, speaker delivery
  - Automatic cleanup of temporary video files
  - Location: `src/analysis/video_analyzer.py`

- **Enhanced Insights**: AI now provides insights based on:
  - Visual storytelling techniques
  - Production quality and professionalism
  - On-screen graphics and text
  - Speaker energy and delivery
  - Editing style and pacing

### Fixed
- **Content ID Precision Issue**: Changed Lark Base `content_id` field from Number to Text
  - Prevents precision loss for 19-digit TikTok IDs
  - Full ID preservation (was losing last 3-4 digits with float conversion)
  - Location: `src/storage/lark_client.py:189`

### Changed
- **Analysis Priority**: Video → Subtitles → Caption (previously Caption → Subtitles)
- **Analysis Time**: ~60-90 seconds per video (increased from ~5-10s for text-only)
  - Trade-off accepted for significantly richer insights

### Tested
- End-to-end pipeline with mock data (4 phases)
- Video download from Apify URLs
- Gemini multimodal video analysis
- Database updates with all strategic fields
- Phase 5 update logic (no duplicate records)

### TODO
- Prompt refinement for analysis output format
- Real Apify integration test (blocked: service outage)
- Performance optimization for batch video processing

## [Previous] - 2025-01-19

### Added
- Modular architecture (core, scraping, analysis, storage)
- Two-stage AI analysis (general + strategic)
- Competitor intelligence focus
- Strategic scoring (0-10)
- Controlled content type taxonomy (9 categories)
- Phase 5 update logic (update existing records)
