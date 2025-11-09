# AIbrary 视频生成系统架构文档 v2.0

**版本**: 2.0 (完全重写)
**日期**: 2025-11-04
**状态**: 设计阶段 - 等待审核
**重要变更**: 全自动化流程 + 正确的 AIbrary 定位

---

## 一、系统概述

### 1.1 AIbrary 定位（重要）
**AIbrary 是什么**:
- AI-powered learning platform that turns **books** into personalized **podcasts** and interactive learning experiences
- 目标用户: lifelong learners seeking flexible **book-based personal development**
- 核心场景: 书籍总结、播客学习、个人成长、生产力提升

**监控的内容类别**:
- Books & Reading (书籍阅读)
- Podcasts & Audio Learning (播客和音频学习)
- Productivity & Habits (生产力和习惯)
- AI in Education (教育科技)
- Upskilling & Career (技能提升和职业)
- Knowledge Management (知识管理)

**不是**: AI/ML 技术讨论平台（之前理解错误）

### 1.2 核心理念：从监控到生产的闭环
将现有的 TikTok 监控数据（strategic_insights, strategic_score, engagement_rate）转化为**全自动化视频生成**的输入：

```
监控 TikTok 爆款内容 → AI 提取成功模式 → AI 生成视频脚本 →
AI 全自动生成视频 → 发布追踪效果 → 反馈优化模式
```

**全自动化要求**:
- ❌ 不使用 Canva 等需要人工操作的工具
- ✅ 使用 API 驱动的 AI 视频生成（Sora 2, Runway Gen-3）
- ✅ 使用 ffmpeg 自动化文字烧录和视频剪辑
- ✅ 使用 ElevenLabs API 自动生成语音
- ✅ Python 脚本端到端自动化

### 1.3 病毒传播设计原则
每个 pipeline 必须考虑病毒性和曝光度：
1. **3 秒 Hook**: 前 3 秒必须抓住注意力
2. **视觉冲击**: 动态视觉、意外元素、情感共鸣
3. **价值清晰**: 15 秒内让人知道"看完能得到什么"
4. **可分享性**: 内容让人想转发给朋友

---

## 二、三条全自动视频生产线

### Pipeline 1: 病毒式 Hook 短视频（15-30秒）

**定位**: 3 秒抓住注意力的病毒式短视频

**精确数据输入来源** (从现有 TikTok_Content 表提取):
```python
# 筛选条件
source_data = TikTok_Content.filter(
    strategic_score >= 7,  # 高质量内容
    engagement_rate >= 5.0,  # 高互动率
    niche_category IN ["Books & Reading", "Productivity & Habits", "Podcasts & Audio Learning"]
)

# 提取字段
inputs = {
    "hook_text": extract_from(strategic_insights, pattern="Hook强度：.*"),  # 提取 hook 技巧
    "topic": caption,  # 视频主题
    "proven_engagement": engagement_rate,  # 市场验证数据
    "style_reference": video_download_url  # 视觉风格参考（可选）
}
```

**全自动化生成流程**:
```
1. AI 提取 Hook 模式
   ├─ 输入: strategic_insights 字段
   ├─ 工具: Gemini 2.5 Flash API
   └─ 输出: "What if you could read 50 books a year in 15 minutes each?"

2. AI 生成视觉背景
   ├─ 方案 A (低成本): DALL-E 3 生成单张图 + ffmpeg 添加 ken burns 动画
   │   成本: $0.04/image
   │   时间: 10 秒生成
   ├─ 方案 B (高质量): Sora 2 生成 5-10 秒动态背景视频
   │   成本: $1.00 (10 秒 × $0.10/秒)
   │   时间: 60-90 秒生成
   └─ 建议: 先用方案 A 测试，爆款再升级方案 B

3. ffmpeg 自动烧录文字
   ├─ 使用 drawtext 滤镜添加动态文字效果
   ├─ 字体: 大号粗体，高对比度颜色
   ├─ 动画: 淡入 + 放大效果（模仿 TikTok 爆款风格）
   └─ 脚本: auto_generate_text_overlay.py

4. ElevenLabs API 生成语音
   ├─ 选择高能量声音（Brian, Antoni）
   ├─ 添加情感标记（emphasis, excitement）
   └─ 成本: ~$0.30/视频

5. ffmpeg 合成最终视频
   └─ 背景视频 + 文字烧录 + 语音旁白 = 最终输出
```

**成本** (方案 A - 推荐起步):
- 图片生成: $0.04
- 语音生成: $0.30
- **总计: ~$0.34/视频**

**制作时间**: 完全自动化，2-3 分钟/视频

**病毒化设计要点**:
- Hook 在前 3 秒出现（文字 + 语音同时冲击）
- 使用反常识、问题句、数字等高吸引力元素
- 视觉简洁但有运动感（避免静态画面）
- 15-30 秒长度适合 TikTok/YouTube Shorts

**真实示例**:
```
来源内容:
  content_id: 7365719492837608707
  caption: "3 books that will change how you learn forever"
  strategic_insights: "1. Hook强度：数字 + 承诺框架（'3 books that will X'）立刻建立期待..."
  strategic_score: 8
  engagement_rate: 6.8%

生成视频:
  hook_text: "What if 3 books could 10x your learning speed?"
  visual: DALL-E 3 生成书架动态光影图
  text_overlay: "3 BOOKS THAT CHANGED EVERYTHING" (大号黄色文字, 黑色描边)
  voiceover: 高能量男声："你知道吗？只需要3本书..."
  duration: 22 秒
```

---

### Pipeline 2: AI 角色对话视频（60-90秒）

**定位**: 两个 AI 生成的角色讨论书籍/学习/成长话题，视觉上有吸引力

**精确数据输入来源** (从现有 TikTok_Content 表提取):
```python
# 筛选条件
source_data = TikTok_Content.filter(
    strategic_score >= 6,  # 中高质量内容
    engagement_rate >= 4.0,  # 有一定热度
    niche_category IN ["Books & Reading", "Podcasts & Audio Learning", "Productivity & Habits"]
)

# 提取字段
inputs = {
    "discussion_topic": caption,  # 讨论主题（书名、技巧、观点）
    "discussion_angles": extract_from(strategic_insights, all_insights),  # 讨论角度
    "engagement_proof": engagement_rate,  # 话题热度验证
    "subtitle_content": subtitle_url  # 可选：提取原视频金句
}
```

**全自动化生成流程**:
```
1. AI 生成对话脚本
   ├─ 输入: discussion_topic + discussion_angles
   ├─ 工具: Gemini 2.5 Flash API
   ├─ 脚本结构:
   │   - 角色 A (好奇型): "我最近看到一个说法..."
   │   - 角色 B (专家型): "对，这个其实很有意思，关键是..."
   │   - 3 轮对话，每轮 20-30 秒
   │   - 最后自然提到 AIbrary ("这就是为什么我用 AIbrary 把书转成播客...")
   └─ 输出: 对话脚本 JSON {role_a: [...], role_b: [...]}

2. AI 生成虚拟角色视频
   ├─ 方案 A (推荐): Sora 2 生成两个一致的 AI 角色
   │   Prompt: "Two friendly people in a modern podcast studio, split screen,
   │             animated conversation, warm lighting, professional but casual"
   │   成本: 60 秒 × $0.10 = $6.00
   │   优势: 完全定制化，一致性高
   ├─ 方案 B (备选): HeyGen/D-ID AI avatars
   │   成本: ~$0.20/分钟 = $1.20 for 60秒
   │   优势: 更成熟，更稳定
   └─ 方案 C (低成本): 使用动画角色图 + 简单口型同步
       成本: $0 (自制或 free assets)

3. ElevenLabs API 生成双人对话
   ├─ 角色 A: 选择年轻活力声音（如 Emily）
   ├─ 角色 B: 选择稳重专业声音（如 Daniel）
   └─ 成本: ~$0.50-0.80/视频 (长文本)

4. ffmpeg 添加文字高亮
   ├─ 在关键金句处添加文字 overlay
   ├─ 例: 当提到书名时，屏幕中央显示书名
   └─ 脚本: auto_add_subtitle_highlights.py

5. ffmpeg 合成最终视频
   ├─ 角色视频 (split screen) + 对话音频 + 文字高亮
   └─ 添加背景音乐 (低音量，不干扰对话)
```

**成本** (方案 B - 稳定性最佳):
- HeyGen avatars: $1.20
- 双人对话语音: $0.70
- **总计: ~$1.90/视频**

**制作时间**: 完全自动化，5-8 分钟/视频

**病毒化设计要点**:
- 开场抛出有争议或有趣的问题 ("你知道为什么大多数人读完书就忘吗？")
- 对话自然，避免 AI 感太强（使用口语化表达）
- 视觉上使用 split-screen 或交替特写，保持动态
- 在讨论中埋入 AIbrary 的使用场景，不硬推销

**真实示例**:
```
来源内容:
  content_id: 7366523218945123456
  caption: "《原子习惯》最被低估的一章"
  strategic_insights: "1. 内容策略：打破常规认知（'最被低估'制造悬念）
                       2. 格式创新：用对话形式降低教育内容的严肃感..."
  niche_category: "Books & Reading"
  engagement_rate: 7.2%

生成视频:
  script:
    A: "你读过《原子习惯》吗？大家都在讲1%的改进..."
    B: "对，但其实第4章才是精华，讲环境设计，很多人跳过了"
    A: "怎么说？"
    B: "书里说，别靠意志力，改变环境就能自动养成习惯。比如..."
    A: "这太实用了！我用 AIbrary 把这章转成播客，通勤时反复听..."
  visual: Split screen, 两个 AI 角色自然对话，温暖色调
  text_overlays: "《原子习惯》第4章" (5秒处), "环境 > 意志力" (30秒处)
  duration: 68 秒
```

---

### Pipeline 3: 电影级书籍总结视频（60秒）

**定位**: 用 AI 生成的 B-roll 制作电影级书籍总结，建立专业形象

**精确数据输入来源** (从现有 TikTok_Content 表提取):
```python
# 筛选条件
source_data = TikTok_Content.filter(
    niche_category = "Books & Reading",  # 只选书籍内容
    strategic_score >= 7,  # 高质量内容
    engagement_rate >= 5.0,  # 高互动率
    video_download_url IS NOT NULL  # 必须有视觉参考视频
)

# 提取字段
inputs = {
    "book_title": extract_from(caption, book_pattern),  # 书名
    "key_insights": extract_from(strategic_insights, all_numbered_insights),  # 核心观点
    "visual_style_reference": video_download_url,  # 用 Gemini Vision 分析风格
    "subtitle_quotes": subtitle_url,  # 提取原视频金句（可选）
    "engagement_proof": engagement_rate  # 市场验证
}
```

**全自动化生成流程**:
```
1. AI 分析视觉风格 + 生成脚本
   ├─ 输入: video_download_url
   ├─ 工具: Gemini 2.5 Flash (Vision)
   ├─ 分析维度:
   │   - 色调和光影风格 ("warm cinematic lighting", "cool minimalist")
   │   - 镜头运动 ("slow zoom in", "static wide shot")
   │   - 剪辑节奏 ("quick cuts every 3 sec" vs "long takes")
   ├─ 输出:
   │   style_description = "Cinematic, warm golden hour lighting, slow camera movements"
   │   script = 3 key book insights, 20 秒/insight
   └─ 总时长: 60 秒脚本

2. 战略性生成 AI B-roll (混合策略降低成本)
   ├─ Insight 1 (0-20秒):
   │   视觉: Sora 2 生成 8 秒 B-roll
   │   Prompt: "{insight_1_visual_description} in {style_description} style"
   │   成本: 8 秒 × $0.10 = $0.80
   │   填充: 12 秒用文字卡片 (ffmpeg) = $0
   ├─ Insight 2 (20-40秒):
   │   视觉: DALL-E 3 静态图 + Ken Burns 动画 (ffmpeg)
   │   成本: $0.04
   │   填充: 剩余时间用文字卡片 = $0
   └─ Insight 3 (40-60秒):
       视觉: Runway Gen-3 生成 8 秒 B-roll
       Prompt: "{insight_3_visual_description}"
       成本: 8 秒 × $0.125 = $1.00
       填充: 12 秒用文字卡片 + outro = $0

   总 AI 视频时长: 16 秒 (27%)
   文字卡片时长: 44 秒 (73%)
   总成本: $0.80 + $0.04 + $1.00 = $1.84

3. ElevenLabs API 生成旁白
   ├─ 选择专业沉稳声音 (如 Josh, Sam)
   ├─ 60 秒脚本, ~150 words
   └─ 成本: ~$0.40

4. ffmpeg 自动化剪辑和烧录
   ├─ 时间线编排:
   │   0-8秒: Sora B-roll + insight 1 旁白
   │   8-20秒: 文字卡片 (白色大号文字, 黑色背景) + 旁白继续
   │   20-28秒: DALL-E 静态图 Ken Burns + insight 2 旁白
   │   28-40秒: 文字卡片 + 旁白
   │   40-48秒: Runway B-roll + insight 3 旁白
   │   48-60秒: 文字卡片 outro ("Try AIbrary to turn this book into a podcast")
   ├─ 文字烧录: drawtext 滤镜，动态淡入淡出
   ├─ 转场效果: fade, crossfade between clips
   └─ 脚本: auto_edit_book_summary.py

5. 最终输出
   └─ 60 秒电影级书籍总结视频，9:16 竖屏格式
```

**成本**:
- AI B-rolls: $1.84
- 语音旁白: $0.40
- **总计: ~$2.24/视频**

**制作时间**: 完全自动化，8-12 分钟/视频 (大部分是 AI 生成等待时间)

**病毒化设计要点**:
- 开场 3 秒必须是最吸引人的 B-roll + hook ("这本书改变了500万人的生活")
- AI B-roll 只用在最重要的 2-3 个视觉冲击点，其他用文字节省成本
- 文字卡片设计要精美（大号字体、高对比度、简洁排版）
- 结尾留悬念或 call-to-action ("用 AIbrary 15分钟听完这本书")

**真实示例**:
```
来源内容:
  content_id: 7367892341234567890
  caption: "《深度工作》为什么大多数人都做错了"
  strategic_insights: "1. 视觉策略：对比剪辑（错误做法 vs 正确做法）强化记忆..."
  niche_category: "Books & Reading"
  engagement_rate: 8.1%
  video_download_url: "https://v16-webapp.tiktok.com/..."

AI 分析视觉风格:
  Gemini Vision 输出: "Dark moody lighting, office environment, slow push-in shots"

生成脚本:
  Insight 1 (0-20s): "深度工作不是关手机那么简单。真正的关键是..."
  Insight 2 (20-40s): "卡尔·纽波特发现，90分钟才是最佳时长..."
  Insight 3 (40-60s): "更重要的是，你需要创造深度工作的'仪式感'..."

生成视频:
  0-8s: Sora 2 B-roll "Person in deep focus, dark office, cinematic lighting"
  8-20s: 文字卡片 "DEEP WORK ≠ 关手机"
  20-28s: DALL-E 图片 "90-minute timer visualization" + Ken Burns zoom
  28-40s: 文字卡片 "90分钟 = 黄金时长"
  40-48s: Runway B-roll "Morning ritual, coffee, notebook, quiet space"
  48-60s: 文字卡片 outro "用 AIbrary 15分钟掌握《深度工作》精华"

  voiceover: 专业男声，节奏适中，强调关键词
  music: 低音量背景音乐，不干扰旁白
  duration: 60 秒
```

## 三、Lark Base 集成设计（极简方案）

### 设计原则
- **最小化新表格**: 只创建 1 个新表，避免学习成本
- **复用现有结构**: 充分利用已有的 TikTok_Content 表
- **易于导航**: 清晰的数据流，一目了然

### 3.1 只新增一个表: Generated_Videos

**作用**: 追踪 AI 生成的视频从创建到发布的全流程

**与现有系统的关系**:
```
TikTok_Content (现有表)
    ↓ (双向链接)
Generated_Videos (新增表)
    ↓ (发布)
TikTok/YouTube/Instagram
```

**完整字段设计**:

| 字段名 | 类型 | 说明 | 填充方式 |
|--------|------|------|---------|
| **基础信息** ||||
| video_id | 文本 (主键) | 自动生成 | `vid_20251104_hook_001` |
| source_content | 双向链接 | 链接到 TikTok_Content 表 | 自动关联 |
| pipeline_type | 单选 | 视频类型 | `Hook短视频`, `AI对话`, `书籍总结` |
| created_date | 日期 | 创建时间 | 自动填充 |
| **生成配置** ||||
| script_text | 多行文本 | AI 生成的脚本 | AI 输出 |
| visual_style | 文本 | 视觉风格描述 | AI 分析结果 |
| voiceover_voice | 单选 | 使用的声音 | `Brian`, `Emily`, `Josh`, `Sam` |
| duration_seconds | 数字 | 视频时长 | 自动计算 |
| **生产状态** ||||
| status | 单选 | 当前状态 | `queued` → `generating` → `ready` → `published` |
| generation_started | 日期时间 | 开始生成时间 | 自动 |
| generation_completed | 日期时间 | 完成时间 | 自动 |
| error_message | 多行文本 | 错误信息（如有） | 系统填充 |
| **成本追踪** ||||
| cost_image_gen | 数字 | 图片生成成本 | 自动 |
| cost_video_gen | 数字 | 视频生成成本 | 自动 |
| cost_voice_gen | 数字 | 语音生成成本 | 自动 |
| total_cost | 数字 | 总成本 (USD) | 自动求和 |
| **输出文件** ||||
| video_file_url | 附件 | 生成的视频文件 | 上传 |
| thumbnail_url | 附件 | 视频缩略图 | 自动生成 |
| **发布追踪** ||||
| publish_platform | 多选 | 发布平台 | `TikTok`, `YouTube Shorts`, `Instagram Reels` |
| publish_url | URL | 发布链接 | 手动/API |
| publish_date | 日期 | 发布日期 | 手动 |
| **效果数据** ||||
| views | 数字 | 观看量 | 定期更新 |
| likes | 数字 | 点赞数 | 定期更新 |
| comments | 数字 | 评论数 | 定期更新 |
| shares | 数字 | 分享数 | 定期更新 |
| engagement_rate | 数字 | 互动率 (%) | 自动计算 |
| performance_tier | 单选 | 表现分级 | `爆款` (>8%), `优秀` (5-8%), `一般` (<5%) |
| **团队协作** ||||
| notes | 多行文本 | 备注 | 团队填写 |

### 3.2 使用视图(Views)组织工作流

在 Generated_Videos 表中创建多个视图，方便团队使用:

**视图 1: 生产队列** (Production Queue)
- 筛选: `status` IN [`queued`, `generating`]
- 排序: `created_date` 升序
- 显示字段: `video_id`, `pipeline_type`, `status`, `generation_started`
- 用途: 监控正在生成的视频

**视图 2: 待发布** (Ready to Publish)
- 筛选: `status` = `ready`
- 排序: `generation_completed` 降序
- 显示字段: `video_id`, `pipeline_type`, `video_file_url`, `script_text`
- 用途: 查看可以发布的视频

**视图 3: 效果分析** (Performance Dashboard)
- 筛选: `status` = `published` AND `publish_date` > 最近30天
- 排序: `engagement_rate` 降序
- 显示字段: `video_id`, `pipeline_type`, `views`, `engagement_rate`, `performance_tier`, `total_cost`
- 分组: 按 `pipeline_type` 分组
- 用途: 分析哪种视频类型效果最好

**视图 4: 成本分析** (Cost Analysis)
- 筛选: `generation_completed` IS NOT NULL
- 显示字段: `video_id`, `pipeline_type`, `total_cost`, `cost_breakdown`
- 统计: 每种 pipeline 的平均成本
- 用途: 控制预算

### 3.3 自动化工作流

**Step 1: 自动选择源内容**
```python
# 脚本: scripts/auto_select_source_content.py
# 每天自动从 TikTok_Content 选择高分内容
# 创建 Generated_Videos 记录，状态 = queued

high_score_content = TikTok_Content.filter(
    strategic_score >= 7,
    engagement_rate >= 5.0,
    not_used_for_generation = True  # 避免重复
).order_by("-engagement_rate").limit(5)

for content in high_score_content:
    Generated_Videos.create(
        source_content=content.record_id,
        pipeline_type=auto_detect_pipeline(content),  # 根据 niche_category 自动判断
        status="queued"
    )
```

**Step 2: 自动生成视频**
```python
# 脚本: scripts/auto_generate_videos.py
# 读取 status = queued 的记录
# 调用 AI APIs 生成视频
# 更新状态到 ready

queued_videos = Generated_Videos.filter(status="queued")

for video in queued_videos:
    video.status = "generating"
    video.save()

    # 调用生成流程
    output = generate_video(
        source_content=video.source_content,
        pipeline_type=video.pipeline_type
    )

    video.video_file_url = output.video_url
    video.total_cost = output.cost
    video.status = "ready"
    video.generation_completed = now()
    video.save()
```

**Step 3: 手动发布 + 自动追踪**
- 团队从"待发布"视图中选择视频
- 发布到 TikTok/YouTube，填写 `publish_url`
- 系统每天自动更新观看数据（通过 API 或手动输入）

### 3.4 数据流示意图

```
┌──────────────────────────┐
│ TikTok_Content (现有)     │  ← 监控系统持续填充
│ strategic_score > 7      │
└────────────┬─────────────┘
             │ (自动选择)
             ↓
┌──────────────────────────┐
│ Generated_Videos (新增)   │
│ status = queued          │  ← 脚本: auto_select_source_content.py
└────────────┬─────────────┘
             │ (自动生成)
             ↓
┌──────────────────────────┐
│ Generated_Videos          │
│ status = ready           │  ← 脚本: auto_generate_videos.py
│ + video_file_url         │
└────────────┬─────────────┘
             │ (手动发布)
             ↓
┌──────────────────────────┐
│ Generated_Videos          │
│ status = published       │  ← 团队操作 + 效果追踪
│ + views, engagement_rate │
└──────────────────────────┘
```

### 3.5 为什么不需要 Content_Patterns 和 Video_Scripts 表？

**原因 1**: 模式可以直接从 strategic_insights 字段实时提取
- 不需要单独存储
- 避免数据冗余
- Generated_Videos 的 script_text 已经包含生成的脚本

**原因 2**: 降低使用复杂度
- 团队只需要关注 2 个表: TikTok_Content → Generated_Videos
- 数据流更直观

**原因 3**: 如果未来需要模式分析
- 可以用 Python 脚本临时分析 Generated_Videos 中的 script_text
- 生成 Excel 报表，不需要持久化存储

---

## 四、完整技术栈和工具清单

### 4.1 AI 生成 APIs

| 工具 | 用途 | Pipeline | 成本 | API文档 |
|------|------|----------|------|---------|
| **Gemini 2.5 Flash** | 脚本生成 + 视觉风格分析 | 全部 | ~$0.02/请求 | [docs](https://ai.google.dev/gemini-api/docs) |
| **DALL-E 3** | 静态图片生成 | Pipeline 1, 3 | $0.04/image | [docs](https://platform.openai.com/docs/guides/images) |
| **Sora 2 API** | 动态视频生成 (高质量) | Pipeline 2, 3 | $0.10/秒 | *需申请* |
| **Runway Gen-3 Turbo** | 动态视频生成 (备选) | Pipeline 2, 3 | $0.125/秒 | [docs](https://docs.runwayml.com) |
| **ElevenLabs TTS** | 语音生成 | 全部 | $0.30/视频 | [docs](https://elevenlabs.io/docs) |
| **HeyGen/D-ID** | AI avatar (备选) | Pipeline 2 | $0.20/分钟 | [HeyGen](https://heygen.com/api), [D-ID](https://docs.d-id.com) |

### 4.2 视频处理工具

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| **ffmpeg** | 文字烧录、视频剪辑、音频合并 | `brew install ffmpeg` |
| **Python libraries** | 自动化脚本 | `pip install openai google-generativeai elevenlabs-python` |

### 4.3 技术架构图

```
┌─────────────────────────────────────────────────────────────┐
│ 输入层: TikTok_Content (现有监控数据)                         │
│ • strategic_insights (策略分析)                              │
│ • engagement_rate (市场验证)                                 │
│ • video_download_url (视觉参考)                              │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 处理层: Python 自动化脚本                                     │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Step 1: auto_select_source_content.py                   │ │
│ │ → 从 TikTok_Content 筛选高分内容                         │ │
│ │ → 创建 Generated_Videos 记录 (status=queued)            │ │
│ └─────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Step 2: auto_generate_videos.py                         │ │
│ │ ├─ Gemini: 生成脚本 + 分析视觉风格                       │ │
│ │ ├─ DALL-E/Sora/Runway: 生成视觉素材                      │ │
│ │ ├─ ElevenLabs: 生成语音                                  │ │
│ │ └─ ffmpeg: 合成最终视频                                  │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 输出层: Generated_Videos (status=ready)                      │
│ • video_file_url (成品视频)                                  │
│ • total_cost (成本追踪)                                      │
│ • script_text (脚本内容)                                     │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 发布层: TikTok / YouTube Shorts / Instagram Reels            │
│ → 团队手动发布或通过平台 API 自动发布                         │
│ → 填写 publish_url, 系统追踪 views/likes/engagement_rate     │
└─────────────────────────────────────────────────────────────┘
```

---

## 五、Week 1 实施计划 (完全自动化 MVP)

### 目标
在 7 天内完成 **Pipeline 1 (Hook短视频)** 的端到端自动化，产出 **3 个真实视频**。

### Day 1: 环境搭建 (2小时)

**任务**:
1. 安装依赖
   ```bash
   brew install ffmpeg
   pip install openai google-generativeai elevenlabs requests
   ```
2. 配置 API keys (.env 文件)
   ```
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=AIza...
   ELEVENLABS_API_KEY=...
   ```
3. 创建 Lark Base 表 `Generated_Videos` (按照 Section 3.1 的字段设计)

**验收**: 成功调用 Gemini API + ElevenLabs API + DALL-E API

---

### Day 2-3: 开发 Pipeline 1 自动化脚本 (6小时)

**脚本 1**: `src/video_generation/pipelines/hook_video_generator.py`

```python
def generate_hook_video(source_content_id: str) -> dict:
    """
    完全自动化生成 Hook 短视频

    输入: TikTok_Content 记录 ID
    输出: {video_url, script, cost, duration}
    """
    # Step 1: 从 Lark Base 读取源内容
    content = lark_client.get_content(source_content_id)

    # Step 2: Gemini 提取 hook + 生成脚本
    script = gemini_generate_hook_script(
        strategic_insights=content.strategic_insights,
        caption=content.caption
    )

    # Step 3: DALL-E 生成背景图
    image_url = dalle_generate_image(
        prompt=f"Inspirational book-learning scene, {script['visual_description']}"
    )
    cost_image = 0.04

    # Step 4: ffmpeg 添加 Ken Burns 动画
    animated_video = ffmpeg_ken_burns_effect(image_url, duration=22)

    # Step 5: ffmpeg 烧录文字
    video_with_text = ffmpeg_burn_text(
        animated_video,
        text=script['hook_text'],
        style="bold_yellow_with_black_stroke"
    )

    # Step 6: ElevenLabs 生成语音
    audio_url = elevenlabs_generate(
        text=script['voiceover_text'],
        voice="Brian"  # 高能量男声
    )
    cost_voice = 0.30

    # Step 7: ffmpeg 合成最终视频
    final_video = ffmpeg_merge_audio_video(video_with_text, audio_url)

    return {
        "video_url": upload_to_storage(final_video),
        "script": script,
        "total_cost": cost_image + cost_voice,
        "duration": 22
    }
```

**脚本 2**: `src/video_generation/auto_generate_videos.py` (主流程)

```python
# 读取 Generated_Videos 表中 status = "queued" 的记录
queued_videos = lark_client.get_queued_videos()

for video in queued_videos:
    try:
        # 更新状态
        video.status = "generating"
        video.save()

        # 调用生成函数
        result = generate_hook_video(video.source_content.id)

        # 保存结果
        video.video_file_url = result['video_url']
        video.script_text = result['script']['full_text']
        video.total_cost = result['total_cost']
        video.duration_seconds = result['duration']
        video.status = "ready"
        video.generation_completed = now()
        video.save()

        print(f"✅ Generated video: {video.video_id}")
    except Exception as e:
        video.error_message = str(e)
        video.status = "queued"  # 重新排队
        video.save()
        print(f"❌ Failed: {e}")
```

**验收**:
- 运行脚本成功生成 1 个测试视频
- 视频包含: 动态背景 + 文字烧录 + 语音旁白
- 成本记录准确

---

### Day 4: 批量生成 3 个视频 (2小时)

**任务**:
1. 从 TikTok_Content 表手动选择 3 条高分内容
2. 在 Generated_Videos 表中创建 3 条 `status=queued` 记录
3. 运行 `auto_generate_videos.py`
4. 等待生成完成（约 15-20 分钟）

**验收**:
- 3 个视频全部生成成功
- 每个视频成本 ~$0.34
- 视频质量可发布

---

### Day 5-6: 优化和测试 (4小时)

**优化项**:
1. **文字烧录效果优化**
   - 尝试不同字体和颜色
   - 添加淡入淡出动画
   - 测试不同文字位置

2. **Hook 提取质量优化**
   - 优化 Gemini prompt
   - 提供 few-shot examples
   - 对比生成质量

3. **语音效果优化**
   - 测试不同声音 (Brian vs Antoni)
   - 调整语速和停顿
   - 添加情感标记

**验收**:
- 重新生成 3 个优化后的视频
- 团队内部评审，选择最佳版本

---

### Day 7: 发布和追踪 (2小时)

**任务**:
1. 选择 1-2 个最佳视频发布到 TikTok
2. 填写 `publish_url` 和 `publish_platform`
3. 设置提醒：3 天后检查播放数据
4. 创建简单的效果追踪 Excel 表格

**验收**:
- 至少 1 个视频成功发布
- Generated_Videos 表中状态更新为 `published`

---

## 六、成本和时间预算

### 6.1 Week 1 实际成本

| 项目 | 单价 | 数量 | 小计 |
|------|------|------|------|
| DALL-E 图片生成 | $0.04 | 6 (含测试) | $0.24 |
| ElevenLabs 语音 | $0.30 | 6 | $1.80 |
| Gemini API 调用 | $0.02 | 10 | $0.20 |
| **总计** | | | **$2.24** |

### 6.2 长期运营成本 (每月)

**假设每月生成 30 个视频 (Pipeline 1)**:
- 图片: 30 × $0.04 = $1.20
- 语音: 30 × $0.30 = $9.00
- Gemini: 30 × $0.02 = $0.60
- **月成本: ~$11/月**

**Pipeline 2 和 3**:
- Pipeline 2 (AI对话): ~$1.90/视频
- Pipeline 3 (书籍总结): ~$2.24/视频

如果混合生成 (10个P1 + 10个P2 + 10个P3):
- **月成本: ~$45-50/月**

---

## 七、关键决策点

### 7.1 Week 1 范围确认
**问题**: 只做 Pipeline 1，还是同时启动 3 个 Pipelines？

**建议**: **只做 Pipeline 1**
- 原因: 快速验证自动化流程可行性
- Pipeline 2 和 3 需要更多视觉生成 (Sora/Runway)，成本和复杂度更高
- Week 1 先把最简单的做通，Week 2 再扩展

### 7.2 Sora 2 API 申请
**问题**: Sora 2 API 目前需要邀请，是否等待？

**备选方案**:
- **方案 A**: 先用 DALL-E + Ken Burns 动画 (Week 1)
- **方案 B**: 申请 Sora 2 access，同时开发，等通过后替换
- **方案 C**: 使用 Runway Gen-3 作为备选（立即可用）

**建议**: 方案 A + B 并行

### 7.3 视频发布策略
**问题**: Week 1 生成的视频是否立即发布？

**建议**: 发布 1-2 个测试市场反应
- 如果 engagement_rate > 4.0: 继续批量生产
- 如果 < 2.0: 暂停，优化 hook 提取和视觉风格

### 7.4 自动化 vs 人工审核
**问题**: 生成的视频是否需要人工审核？

**建议**: Week 1-2 需要人工审核
- 检查脚本质量
- 检查文字烧录是否清晰
- 检查语音节奏是否自然
- 等系统稳定后再完全自动化

---

## 八、风险缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| API 调用失败 | 中 | 高 | 添加重试逻辑 + error handling |
| 生成视频质量差 | 中 | 高 | 人工审核 + prompt 优化 |
| ffmpeg 脚本bug | 高 | 中 | 充分测试 + 保留中间文件方便 debug |
| 成本超支 | 低 | 中 | 每个视频生成前预估成本，设置上限 |
| Sora 2 API 未获批 | 高 | 低 | 使用 Runway/DALL-E 作为备选 |

---

## 九、下一步行动

### 立即确认 (等待你的反馈):
1. ✅ Week 1 只做 Pipeline 1？
2. ✅ 使用 DALL-E + ffmpeg，不等 Sora 2？
3. ✅ 生成 3 个视频后先内部评审再发布？
4. ✅ Generated_Videos 表字段设计是否OK？

### 确认后立即开始:
1. Day 1: 环境搭建和 API 测试
2. Day 2-3: 开发 `hook_video_generator.py`
3. Day 4: 生成 3 个视频
4. Day 5-6: 优化效果
5. Day 7: 发布测试

---

**文档状态**: v2.0 待审核
**下一个里程碑**: Week 1 完成 Pipeline 1 自动化，产出 3 个视频
**预计时间**: 2025-11-11 (7天后)
