# AIbrary System Architecture (三层架构)

**Version**: 1.0
**Date**: 2025-11-08
**Purpose**: Complete system architecture from monitoring → analysis → AIGC

---

## 一、系统概览 (System Overview)

```
┌─────────────────────────────────────────────────────────────────┐
│                        AIbrary 内容生态系统                        │
│                   (Content Ecosystem)                            │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │   TikTok     │  External Data Source
    │  Viral Data  │
    └──────┬───────┘
           │
           ↓
┌──────────────────────────────────────────────────────────────────┐
│  第一层: 监控层 (Layer 1: Monitoring)                              │
│  Purpose: Scrape and filter high-quality content                 │
│  ────────────────────────────────────────────────────────────    │
│  • Apify Integration (scraping/*)                                │
│  • Quality Filtering (filtering/*)                               │
│  • Data Storage (storage/lark_client.py)                         │
│                                                                   │
│  Output: TikTok_Content table (Lark Base)                        │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ↓
┌──────────────────────────────────────────────────────────────────┐
│  第二层: 分析层 (Layer 2: Analysis)                                │
│  Purpose: Extract strategic insights from content                │
│  ────────────────────────────────────────────────────────────    │
│  • AI Analysis (analysis/video_analyzer.py)                      │
│  • Prompt Engineering (analysis/prompts.py)                      │
│  • Response Parsing (analysis/parsers.py)                        │
│                                                                   │
│  Output: strategic_insights, strategic_score, niche_category     │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ↓
┌──────────────────────────────────────────────────────────────────┐
│  第三层: AIGC 层 (Layer 3: AI Generated Content)                   │
│  Purpose: Generate new content based on proven patterns          │
│  ────────────────────────────────────────────────────────────    │
│  • Pipeline Orchestration (aigc/orchestrator.py)                 │
│  • AI Agents (aigc/agents/*)                                     │
│  • Content Generators (aigc/generators/*)                        │
│  • Multiple Pipelines (aigc/pipelines/*)                         │
│                                                                   │
│  Output: Generated_Videos table (Lark Base)                      │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ↓
                  ┌────────────┐
                  │ Publishing │  TikTok, YouTube, Instagram
                  └────────────┘
```

---

## 二、目录结构设计 (Directory Structure)

### 2.1 Current Structure (Layers 1-2) ✅ IMPLEMENTED

```
src/
├── shared/                     # 核心共享组件 (Shared across all layers)
│   ├── core/                  # Data models and configuration
│   │   ├── __init__.py
│   │   ├── config.py          # Environment variables, API keys
│   │   └── models.py          # Data models (MonitoringTarget, TikTokContent, FilterRule)
│   │
│   └── storage/               # Data persistence
│       ├── __init__.py
│       └── lark_client.py     # Lark Base API client
│
├── layer1_monitoring/          # 第一层: 监控层 (Scraping + Filtering)
│   ├── scraping/              # Content acquisition
│   │   ├── __init__.py
│   │   ├── base.py            # BaseProcessor abstract class
│   │   ├── factory.py         # Processor factory pattern
│   │   ├── profile_processor.py  # TikTok profile scraping
│   │   ├── hashtag_processor.py  # Hashtag scraping
│   │   └── search_processor.py   # Search term scraping
│   │
│   ├── filtering/             # Quality control
│   │   ├── __init__.py
│   │   ├── rule_matcher.py    # Hierarchical rule matching
│   │   └── content_filter.py  # OR logic filtering + metrics
│   │
│   └── orchestrator.py        # Layer 1 orchestrator
│
├── layer2_analysis/            # 第二层: 分析层 (AI Analysis)
│   ├── __init__.py
│   ├── video_analyzer.py      # Main analyzer (Gemini integration)
│   ├── prompts.py             # Strategy-aware prompts
│   └── parsers.py             # Response parsing
│
├── layer3_aigc/                # 第三层: AIGC 生成层 (Planned)
│   └── (to be implemented)    # Content generation pipelines
│
└── run_monitoring.py           # Main entry point (Layers 1 + 2)
```

### 2.2 Proposed AIGC Layer (Layer 3) - PLANNED

```
src/
├── layer3_aigc/                # 第三层: AIGC 生成层 (PLANNED)
│   │
│   ├── __init__.py
│   ├── orchestrator.py         # Main AIGC orchestrator
│   │                           # - Reads from TikTok_Content
│   │                           # - Routes to appropriate pipeline
│   │                           # - Saves to Generated_Videos
│   │
│   ├── models.py              # AIGC-specific data models
│   │                           # - GeneratedVideo
│   │                           # - Character
│   │                           # - SceneDescription
│   │                           # - PipelineConfig
│   │
│   ├── agents/                 # AI Agents for content generation
│   │   ├── __init__.py
│   │   ├── base_agent.py      # BaseAgent abstract class
│   │   ├── scene_agent.py     # Converts strategic_insights → scene descriptions
│   │   ├── script_agent.py    # Generates video scripts
│   │   └── dialogue_agent.py  # Extracts/generates dialogue from subtitles
│   │
│   ├── generators/             # API integrations for content generation
│   │   ├── __init__.py
│   │   ├── base_generator.py  # BaseGenerator abstract class
│   │   ├── sora_generator.py  # Sora 2 API integration
│   │   ├── image_generator.py # DALL-E 3 / Stable Diffusion
│   │   ├── voice_generator.py # ElevenLabs TTS
│   │   └── video_editor.py    # ffmpeg wrapper for post-processing
│   │
│   ├── pipelines/              # Content generation pipelines
│   │   ├── __init__.py
│   │   ├── base_pipeline.py   # BasePipeline abstract class
│   │   │
│   │   ├── sora_cameo/        # Pipeline 1: Sora Character Cameo Videos
│   │   │   ├── __init__.py
│   │   │   ├── pipeline.py    # Main cameo pipeline orchestrator
│   │   │   ├── character_library.py  # Character definitions & mapping
│   │   │   └── config.py      # Cameo-specific configuration
│   │   │
│   │   ├── podcast/           # Pipeline 2: AI Dialogue Podcasts
│   │   │   ├── __init__.py
│   │   │   ├── pipeline.py
│   │   │   └── config.py
│   │   │
│   │   ├── hook_video/        # Pipeline 3: Hook Short Videos
│   │   │   ├── __init__.py
│   │   │   ├── pipeline.py
│   │   │   └── config.py
│   │   │
│   │   └── book_summary/      # Pipeline 4: Book Summary Videos
│   │       ├── __init__.py
│   │       ├── pipeline.py
│   │       └── config.py
│   │
│   └── utils/                  # AIGC utilities
│       ├── __init__.py
│       ├── media_utils.py     # Video/audio/image processing helpers
│       ├── prompt_templates.py # Reusable prompt templates
│       └── cost_tracker.py    # API cost tracking
```

---

## 三、数据流设计 (Data Flow Architecture)

### 3.1 Complete Data Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: Monitoring (监控)                                        │
└─────────────────────────────────────────────────────────────────┘

Input:  Monitoring_Targets table
        ↓
Process: layer1_monitoring/scraping/* → layer1_monitoring/filtering/*
        ↓
Output: TikTok_Content table (raw + filtered)

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: Analysis (分析)                                          │
└─────────────────────────────────────────────────────────────────┘

Input:  TikTok_Content (filtered records)
        ↓
Process: layer2_analysis/video_analyzer.py
        ├─ Gemini Vision API
        ├─ Strategy-aware prompts
        └─ Response parsing
        ↓
Output: TikTok_Content (+ strategic_insights, strategic_score, niche_category)

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: AIGC Generation (生成)                                   │
└─────────────────────────────────────────────────────────────────┘

Input:  TikTok_Content (high-score records, score >= 7)
        ↓
Process: layer3_aigc/orchestrator.py
        ├─ Select source content
        ├─ Route to appropriate pipeline
        │   ├─ layer3_aigc/pipelines/sora_cameo/pipeline.py
        │   ├─ layer3_aigc/pipelines/podcast/pipeline.py
        │   ├─ layer3_aigc/pipelines/hook_video/pipeline.py
        │   └─ layer3_aigc/pipelines/book_summary/pipeline.py
        ├─ AI agents generate prompts/scripts
        ├─ API generators create media
        └─ Save results
        ↓
Output: Generated_Videos table

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: Publishing (发布)                                        │
└─────────────────────────────────────────────────────────────────┘

Input:  Generated_Videos (status = ready)
        ↓
Process: Manual or automated publishing
        ↓
Output: TikTok/YouTube/Instagram + performance tracking
```

### 3.2 Data Contract Between Layers

**Layer 1 → Layer 2**:
```python
# TikTok_Content after monitoring (minimum required fields)
{
    "content_id": str,
    "video_url": str,
    "caption": str,
    "video_download_url": str,  # For Gemini Vision
    "subtitle_url": str,         # For context analysis
    "engagement_rate": float     # Quality indicator
}
```

**Layer 2 → Layer 3**:
```python
# TikTok_Content after analysis (AIGC input)
{
    # Original monitoring data
    "content_id": str,
    "caption": str,
    "video_download_url": str,
    "subtitle_url": str,
    "engagement_rate": float,

    # Analysis outputs (NEW)
    "strategic_score": int,          # 0-10, filter >= 7 for AIGC
    "strategic_insights": str,       # 2-3 numbered tactics
    "niche_category": str,          # Character/style selection
    "content_type": str             # Optional: content classification
}
```

**Layer 3 Output**:
```python
# Generated_Videos (NEW table)
{
    "video_id": str,
    "source_content_id": str,        # Links back to TikTok_Content
    "pipeline_type": str,            # "sora_cameo", "podcast", etc.
    "script_text": str,              # Generated script
    "video_file_url": str,           # Final video
    "generation_config": dict,       # API params used
    "total_cost": float,             # USD
    "status": str,                   # queued/generating/ready/published
    "created_date": datetime
}
```

---

## 四、核心组件设计 (Core Component Design)

### 4.1 AIGC Orchestrator (layer3_aigc/orchestrator.py)

**Responsibility**: Main entry point for AIGC layer

```python
class AIGCOrchestrator:
    """
    Orchestrates AI content generation from monitored TikTok data
    """

    def __init__(self, lark_client: LarkClient):
        self.lark = lark_client
        self.pipelines = self._load_pipelines()

    def generate_content(
        self,
        pipeline_name: str,
        source_content_ids: List[str] = None,
        auto_select: bool = True,
        config: dict = None
    ) -> List[GeneratedVideo]:
        """
        Main generation method

        Args:
            pipeline_name: "sora_cameo", "podcast", etc.
            source_content_ids: Specific TikTok content to use (optional)
            auto_select: Auto-select high-score content (default True)
            config: Pipeline-specific configuration

        Returns:
            List of generated video records
        """
        # 1. Select source content
        if auto_select:
            source_content = self._auto_select_content(pipeline_name)
        else:
            source_content = self.lark.get_content_by_ids(source_content_ids)

        # 2. Route to pipeline
        pipeline = self.pipelines[pipeline_name]

        # 3. Generate content
        results = []
        for content in source_content:
            try:
                video = pipeline.generate(content, config)
                results.append(video)
            except Exception as e:
                logger.error(f"Failed to generate from {content.content_id}: {e}")

        # 4. Save to Lark Base
        self.lark.save_generated_videos(results)

        return results

    def _auto_select_content(self, pipeline_name: str) -> List[TikTokContent]:
        """
        Auto-select high-quality content for pipeline

        Selection criteria:
        - strategic_score >= 7
        - Has required fields (video_download_url, subtitle_url)
        - Matches pipeline's niche preferences
        - Not already used for generation (avoid duplicates)
        """
        # Implementation here
        pass
```

### 4.2 Base Pipeline (layer3_aigc/pipelines/base_pipeline.py)

**Responsibility**: Abstract base class for all pipelines

```python
from abc import ABC, abstractmethod

class BasePipeline(ABC):
    """
    Abstract base class for AIGC pipelines
    """

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.agents = self._initialize_agents()
        self.generators = self._initialize_generators()

    @abstractmethod
    def generate(self, source_content: TikTokContent, config: dict = None) -> GeneratedVideo:
        """
        Generate content from TikTok source

        Must implement:
        1. Prepare inputs from source_content
        2. Use agents to generate prompts/scripts
        3. Use generators to create media
        4. Return GeneratedVideo object
        """
        pass

    @abstractmethod
    def _initialize_agents(self) -> dict:
        """
        Initialize AI agents needed for this pipeline
        Returns: {"agent_name": AgentInstance}
        """
        pass

    @abstractmethod
    def _initialize_generators(self) -> dict:
        """
        Initialize API generators needed for this pipeline
        Returns: {"generator_name": GeneratorInstance}
        """
        pass

    def validate_source(self, source_content: TikTokContent) -> bool:
        """
        Validate if source content is suitable for this pipeline
        Override in subclass for pipeline-specific validation
        """
        return (
            source_content.strategic_score >= 7 and
            source_content.video_download_url and
            source_content.strategic_insights
        )
```

### 4.3 Base Agent (layer3_aigc/agents/base_agent.py)

**Responsibility**: Abstract base class for AI agents

```python
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract base class for AI agents
    Agents convert data → prompts/scripts
    """

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model
        self.client = self._initialize_client()

    @abstractmethod
    def process(self, input_data: dict) -> dict:
        """
        Process input data and return structured output

        Args:
            input_data: Dict with agent-specific inputs

        Returns:
            Dict with agent-specific outputs
        """
        pass

    @abstractmethod
    def _initialize_client(self):
        """Initialize AI model client (Gemini, GPT, etc.)"""
        pass
```

### 4.4 Base Generator (layer3_aigc/generators/base_generator.py)

**Responsibility**: Abstract base class for API generators

```python
from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    """
    Abstract base class for content generators
    Generators call APIs to create media (video, audio, images)
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.client = self._initialize_client()

    @abstractmethod
    def generate(self, prompt: str, config: dict = None) -> str:
        """
        Generate media from prompt

        Args:
            prompt: Text prompt or structured input
            config: Generator-specific configuration

        Returns:
            URL or file path to generated media
        """
        pass

    @abstractmethod
    def estimate_cost(self, config: dict) -> float:
        """
        Estimate generation cost in USD
        """
        pass
```

---

## 五、Lark Base 表格设计 (Database Schema)

### 5.1 Existing Tables (Layers 1-2)

1. **Monitoring_Targets** - Input configuration
2. **Filter_Rules** - Quality control rules
3. **TikTok_Content** - Scraped and analyzed content

### 5.2 New Tables (Layer 3)

#### Generated_Videos (主表)

| Field | Type | Description | Auto-populated? |
|-------|------|-------------|-----------------|
| video_id | Text (PK) | Unique identifier | ✅ Auto |
| source_content | Link | → TikTok_Content | ✅ Auto |
| pipeline_type | Single Select | "sora_cameo", "podcast", etc. | ✅ Auto |
| script_text | Long Text | Generated script | ✅ Auto |
| scene_description | Long Text | Sora prompt | ✅ Auto |
| video_file_url | Attachment | Final video | ✅ Auto |
| thumbnail_url | Attachment | Video thumbnail | ✅ Auto |
| duration_seconds | Number | Video length | ✅ Auto |
| status | Single Select | queued/generating/ready/published | ✅ Auto |
| cost_breakdown | Long Text | JSON cost details | ✅ Auto |
| total_cost | Number | USD | ✅ Auto |
| generation_started | DateTime | Start time | ✅ Auto |
| generation_completed | DateTime | End time | ✅ Auto |
| error_message | Long Text | Error details (if any) | ✅ Auto |
| publish_platform | Multi-Select | TikTok/YouTube/Instagram | Manual |
| publish_url | URL | Published video link | Manual |
| publish_date | Date | Publication date | Manual |
| views | Number | View count | Manual/API |
| likes | Number | Like count | Manual/API |
| engagement_rate | Number | Calculated % | ✅ Auto |
| notes | Long Text | Team notes | Manual |

#### Characters (Character Library - Optional)

| Field | Type | Description |
|-------|------|-------------|
| character_id | Text (PK) | Unique ID |
| character_name | Text | Display name |
| cameo_username | Text | Sora cameo username (if applicable) |
| niche_category | Single Select | Books/Podcasts/Productivity/etc. |
| personality | Long Text | Character description |
| visual_style | Long Text | Appearance description |
| voice_profile | Text | ElevenLabs voice ID |
| reference_image_url | Attachment | Character reference image |
| active | Checkbox | Is available for use? |

---

## 六、开发优先级 (Development Priorities)

### Phase 1: Foundation - ✅ COMPLETE (2025-11-08)
✅ Layer 1: Monitoring (layer1_monitoring/scraping/, layer1_monitoring/filtering/)
✅ Layer 2: Analysis (layer2_analysis/)
✅ Three-layer architecture reorganization
✅ All imports updated to new structure
✅ End-to-end pipeline tested and working
⬜ Layer 3: Base architecture (NEXT)
- [ ] Create `src/layer3_aigc/` directory structure
- [ ] Implement base classes (BasePipeline, BaseAgent, BaseGenerator)
- [ ] Create Generated_Videos table in Lark Base
- [ ] Implement AIGC orchestrator skeleton

### Phase 2: First Pipeline (Week 1-2) - NEXT
⬜ Sora Cameo Pipeline
- [ ] Define character library
- [ ] Implement SceneAgent (strategic_insights → scene descriptions)
- [ ] Implement SoraGenerator (API integration)
- [ ] Test end-to-end: TikTok_Content → Generated sora video

### Phase 3: Additional Pipelines (Week 2-3)
⬜ Hook Video Pipeline
⬜ Podcast Pipeline
⬜ Book Summary Pipeline

### Phase 4: Optimization (Week 3-4)
⬜ Cost optimization
⬜ Quality improvements
⬜ Batch processing
⬜ Performance tracking

---

## 七、关键设计原则 (Key Design Principles)

### 7.1 Separation of Concerns (关注点分离)
- **Layers**: Monitoring → Analysis → AIGC (清晰分层)
- **Agents**: Data processing, NO API calls
- **Generators**: API calls ONLY, NO business logic
- **Pipelines**: Orchestration, combines agents + generators

### 7.2 Extensibility (可扩展性)
- New pipelines: Inherit from BasePipeline
- New agents: Inherit from BaseAgent
- New generators: Inherit from BaseGenerator
- No changes to core orchestrator needed

### 7.3 Data Traceability (数据可追溯)
- Every Generated_Video links back to source TikTok_Content
- Cost tracking at every step
- Error logging for debugging
- Status tracking for monitoring

### 7.4 Configuration Over Code (配置优于代码)
- Pipeline configs in separate files
- Character library as data, not hardcoded
- API keys in environment variables
- Prompts as templates, not inline strings

---

## 八、下一步行动 (Next Steps)

### ✅ Completed (2025-11-08)
1. ✅ Three-layer architecture reorganization
2. ✅ Layers 1-2 working end-to-end
3. ✅ All documentation updated (README.md, ARCHITECTURE.md)
4. ✅ Pipeline tested with real data

### Immediate (TODAY)
5. ⬜ Create `src/layer3_aigc/` directory structure
6. ⬜ Define character library (5-10 characters)
7. ⬜ Create base classes (BasePipeline, BaseAgent, BaseGenerator)

### This Week
8. ⬜ Implement SceneAgent
9. ⬜ Implement SoraGenerator
10. ⬜ Build Sora Cameo Pipeline
11. ⬜ Test with 3-5 TikTok records

### Next Week
12. ⬜ Build remaining pipelines
13. ⬜ Optimize and batch process
14. ⬜ Deploy and monitor

---

**Status**: Architecture implemented (Layers 1-2 complete), Layer 3 ready to build
**Last Updated**: 2025-11-08
