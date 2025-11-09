# AIbrary Monitoring Layer Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-08

## Active Technologies
- Python 3.13.7 (Three-layer architecture)

## Project Structure (Three-Layer Architecture)
```
src/
├── shared/                  # Core models + storage
│   ├── core/               # Data models, config
│   └── storage/            # Lark Base client
│
├── layer1_monitoring/       # Scraping + Filtering
│   ├── scraping/           # Profile, Hashtag, Search processors
│   ├── filtering/          # Quality filtering
│   └── orchestrator.py     # Layer 1 orchestrator
│
├── layer2_analysis/         # AI Analysis
│   ├── video_analyzer.py   # Gemini-powered analysis
│   ├── prompts.py          # Strategy-specific prompts
│   └── parsers.py          # Response parsing
│
├── layer3_aigc/            # AIGC Generation (planned)
│   └── (to be implemented)
│
└── run_monitoring.py        # Main entry point (Layers 1+2)

tests/
```

## Main Commands
- **Run pipeline**: `python3 src/run_monitoring.py`
- **Test**: `pytest`
- **Lint**: `ruff check .`

## Code Style
Python 3.13.7: Follow standard conventions

## Architecture Principles
- **Separation of Concerns**: Clear layer boundaries (monitoring → analysis → AIGC)
- **Shared Modules**: Common code in `shared/` (no duplication)
- **Import Convention**: Always use `from shared.core import ...`, `from layer1_monitoring import ...`
- **Extensibility**: New processors inherit from base classes

## Recent Changes
- 2025-11-08: Reorganized to three-layer architecture (Layers 1-2 complete, Layer 3 planned)
- 2025-10-21: Added pre-save quality filtering (Feature 006)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->