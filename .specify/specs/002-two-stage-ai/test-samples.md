# Real Content Testing for Two-Stage AI Analysis

Testing approach: Use real TikTok content from new monitoring targets (1 result each) to validate both monitoring pipeline and AI analysis upgrades simultaneously.

## Validation Criteria (Mechanics Only)

### Single API Call Test
- Each sample should generate exactly 1 API call
- Both general analysis and strategic fields should be populated
- Total processing time should be <10 seconds per sample

### Field Population Test
- `Analysis` column gets general content description
- `relevance_score` gets numeric value (0-10)
- `strategic_value` gets numeric value (0-10)
- `content_type` gets category string
- `strategic_insights` gets text under 500 characters

### Database Integration Test
- Content saves successfully to Lark Base
- All fields map correctly to database columns
- No API errors or field mismatches