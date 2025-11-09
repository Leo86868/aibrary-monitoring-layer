# AIbrary Lark Base 使用指南

**最后更新**: 2025-10-31

---

## 📌 系统介绍

AIbrary 是一个 TikTok 内容监控系统，通过 AI 分析帮助你：
- 追踪竞争对手的产品和营销策略
- 学习其他领域的内容创作技巧
- 发现热门趋势和病毒式内容

**你的工作**: 通过 Lark Base 的 3 个表格配置系统

---

## 🗂️ 三个表格说明

1. **Monitoring_Targets** (监控目标) - 告诉系统要监控什么
2. **Filter_Rules** (过滤规则) - 控制内容质量，过滤垃圾信息
3. **TikTok_Content** (内容结果) - 查看收集的内容和 AI 分析

### 表格关系和数据流向

```
┌─────────────────────────────────────────────────────┐
│  你配置（输入）                                        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  📋 Monitoring_Targets (监控目标)                    │
│  ├─ 监控什么: @blinkist, #book                       │
│  ├─ 监控策略: Competitor Intelligence               │
│  └─ 抓取数量: 30条                                   │
│                                                      │
│  🔍 Filter_Rules (过滤规则)                          │
│  ├─ 质量标准: 点赞≥1000 OR 播放≥10000               │
│  ├─ 适用范围: Niche Deep-Dive + profile             │
│  └─ 目的: 过滤低质量内容                             │
│                                                      │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────┐
│  系统自动工作（处理）                                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  1️⃣ 读取 Monitoring_Targets → 找到活跃目标          │
│  2️⃣ 从 TikTok 抓取内容 (via Apify)                  │
│  3️⃣ 读取 Filter_Rules → 匹配规则                    │
│  4️⃣ 过滤内容 (OR逻辑判断)                           │
│  5️⃣ 保存通过的内容 → TikTok_Content                │
│  6️⃣ AI 分析 (根据监控策略路由到不同提示词)           │
│  7️⃣ 更新 AI 分析结果 → TikTok_Content               │
│                                                      │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────┐
│  你查看（输出）                                        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  📊 TikTok_Content (内容结果)                        │
│  ├─ 基础信息: 视频链接、作者、描述                    │
│  ├─ 互动数据: 点赞、评论、播放量                      │
│  ├─ AI 分析: 战略评分、内容类型、关键洞察             │
│  └─ 来源追溯: 链接回 Monitoring_Targets             │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**关键连接点**:
- `Monitoring_Targets` 的 `monitoring_strategy` → 决定 AI 分析用哪个提示词
- `Filter_Rules` 的 `monitoring_strategy + target_type` → 匹配到具体目标
- `TikTok_Content` 的 `Target` 字段 → 链接回原始监控目标

---

## 📋 表格 1: Monitoring_Targets (监控目标)

### 作用
告诉系统要监控哪些 TikTok 账号或话题标签。

### 如何添加监控目标

**步骤**:
1. 打开 `Monitoring_Targets` 表格
2. 点击底部 "+" 添加新行
3. 填写以下字段
4. 勾选 `active` 启动监控

### 字段说明

| 字段 | 填什么 | 示例 |
|------|--------|------|
| **target_value** | 要监控的账号或标签 | `@blinkist` 或 `#book` |
| **platform** | 平台类型 | 填 `tiktok` |
| **target_type** | 目标类型 | `profile` (账号) 或 `hashtag` (标签) |
| **monitoring_strategy** | 监控策略（下面详细说明） | `Competitor Intelligence` 或 `Niche Deep-Dive` |
| **active** | 是否启用 | ✓ 勾选 |
| **results_limit** | 每次抓取数量 | `30` (建议 30-50) |
| **team_notes** | 备注 | 为什么监控这个目标 |

### 监控策略详解

#### 为什么要分三种监控策略？

不同的监控目的需要不同的分析视角：

**问题背景**:

你监控 `@blinkist`（竞品）和 `#book`（书籍话题）时，关注点完全不同：
- 看竞品 → 关心"他们推什么功能"、"用什么话术"（防御性情报）
- 看话题 → 关心"什么内容形式火"、"用什么hooks"（学习创作策略）

如果用同一个 AI 提示词分析，会导致：
- ❌ 分析竞品时，给你内容创作建议（你不需要）
- ❌ 分析话题时，给你产品功能对比（不相关）

**解决方案: 策略路由**

系统根据 `monitoring_strategy` 字段，使用不同的 AI 提示词：

| 策略 | 分析重点 | AI 输出 | 使用场景 |
|------|---------|---------|---------|
| Competitor Intelligence | 产品和营销策略 | 功能卖点、话术分析、竞品对比 | 产品调研、竞品追踪 |
| Niche Deep-Dive | 内容创作策略 | hooks技巧、视频格式、互动策略 | 内容创作、学习爆款 |
| Trend Discovery | 病毒传播机制 | 趋势信号、话题热度、传播速度 | 热点捕捉、机会发现 |

**核心价值**: 一个系统，三种视角，自动路由到正确的分析逻辑。

---

系统支持 3 种监控策略，每种策略的 AI 分析重点不同：

#### 1️⃣ Competitor Intelligence (竞争对手情报)

**用途**: 监控直接竞争对手

**分析重点**:
- 他们推广什么产品功能？
- 用什么营销话术？
- 用户反馈如何？
- 我们可以学习什么？

**适合监控**:
- 直接竞争对手的官方账号
- 例如: `@blinkist`, `@headway.app`, `@audible`

**配置示例**:
```
target_value: @blinkist
target_type: profile
monitoring_strategy: Competitor Intelligence
results_limit: 30
team_notes: 直接竞品 - 书籍总结 app
```

---

#### 2️⃣ Niche Deep-Dive (细分领域深度学习)

**用途**: 学习相关领域的内容创作策略

**分析重点**:
- 他们用什么开头吸引人？
- 视频格式和结构是什么？
- 如何提高互动率？
- 哪些内容策略可以借鉴到 AI/教育领域？

**适合监控**:
- 相关领域的优质创作者（生产力工具、学习 app 等）
- 相关话题标签（书籍、学习、播客等）

**配置示例 - 账号**:
```
target_value: @notionhq
target_type: profile
monitoring_strategy: Niche Deep-Dive
results_limit: 30
team_notes: 相关工具 - 学习他们的内容策略
```

**配置示例 - 标签**:
```
target_value: #book
target_type: hashtag
monitoring_strategy: Niche Deep-Dive
results_limit: 50
team_notes: 书籍社区 - 内容创作灵感
```

---

#### 3️⃣ Trend Discovery (趋势发现) 🚧

**状态**: 基础设施已就绪，AI 分析提示词待实现

**用途**: 追踪 AI/机器学习领域的热门和病毒内容

**计划监控**:
- 广泛话题标签: `#ai`, `#machinelearning`, `#chatgpt`
- 热点关键词: "ChatGPT-4 发布", "OpenAI Sora" 等

---

### ✅ 配置示例总结

**竞争对手监控**:
| target_value | target_type | monitoring_strategy | results_limit |
|--------------|-------------|---------------------|---------------|
| @blinkist | profile | Competitor Intelligence | 30 |
| @headway.app | profile | Competitor Intelligence | 30 |

**细分领域学习**:
| target_value | target_type | monitoring_strategy | results_limit |
|--------------|-------------|---------------------|---------------|
| @notionhq | profile | Niche Deep-Dive | 30 |
| @elsaspeak | profile | Niche Deep-Dive | 30 |
| #book | hashtag | Niche Deep-Dive | 50 |
| #productivity | hashtag | Niche Deep-Dive | 50 |

---

### 💡 使用建议

**账号 vs 标签**:
- **账号 (profile)**: 针对性强，内容稳定，适合追踪特定创作者
- **标签 (hashtag)**: 覆盖面广，内容多样，需要更严格的过滤规则

**results_limit 设置**:
- 账号监控: 30 个足够（一般账号发布频率不高）
- 标签监控: 50-100 个（内容量大，需要过滤）

**监控策略选择**:
- 直接竞品 → `Competitor Intelligence`
- 相关领域/工具 → `Niche Deep-Dive`
- 不确定？→ 先用 `Niche Deep-Dive`（分析更通用）

---

## 🔍 表格 2: Filter_Rules (过滤规则)

### 作用
在内容保存到数据库**之前**过滤掉低质量内容，避免垃圾信息。

### 为什么需要过滤？
- **问题**: 抓取 100 条内容，可能有 50 条是低互动、过时或垃圾内容
- **解决**: 只保存高质量内容，节省存储空间和 AI 分析成本
- **效果**: 实际测试中过滤掉 46.7% 的低质量内容

### 过滤原理

系统使用 **OR 逻辑**判断内容是否通过：

```
内容通过条件 = 点赞数 ≥ 阈值 OR 播放量 ≥ 阈值 OR 互动率 ≥ 阈值

✅ 满足任意一个条件 → 保存并分析
❌ 所有条件都不满足 → 跳过（不保存）
```

**示例**:
```
规则: min_likes = 1000, min_views = 10000

内容 A: 2000 赞 + 5000 播放 → ✅ 通过（点赞数满足）
内容 B: 500 赞 + 15000 播放 → ✅ 通过（播放量满足）
内容 C: 500 赞 + 5000 播放 → ❌ 不通过（都不满足）
```

### 如何添加过滤规则

**步骤**:
1. 打开 `Filter_Rules` 表格
2. 点击底部 "+" 添加新行
3. 填写以下字段
4. 勾选 `active` 启用规则

### 字段说明

| 字段 | 填什么 | 什么时候填 |
|------|--------|------------|
| **monitoring_strategy** | 监控策略 | **必填**，选择 `Competitor Intelligence` 或 `Niche Deep-Dive` |
| **target_type** | 目标类型 | 可选，填 `profile` 或 `hashtag`（留空 = 适用于所有类型） |
| **target_value** | 具体目标 | 可选，填具体账号/标签如 `@blinkist`（通常留空） |
| **min_likes** | 最低点赞数 | 根据需要设置，例如 `1000` |
| **min_views** | 最低播放量 | 根据需要设置，例如 `10000` |
| **min_engagement_rate** | 最低互动率(%) | 可选，例如 `2.5` 表示 2.5% |
| **max_age_days** | 最多天数 | 可选，例如 `30` 表示只要 30 天内的内容 |
| **active** | 是否启用 | ✓ 勾选 |

### 规则匹配逻辑（层级匹配）

系统用**三个字段组合**来匹配规则，按照**从具体到通用**的顺序查找：

| 层级 | 匹配字段 | 说明 |
|------|----------|------|
| **层级 3** | 策略 + 类型 + 具体目标 | 最具体，只对特定目标生效 |
| **层级 2** | 策略 + 类型 | 中等，对某类目标生效 |
| **层级 1** | 策略 | 最通用，对整个策略生效 |

**工作原理**:

系统拿到一个目标（比如 `@elsaspeak, profile, Niche Deep-Dive`），会这样查找：

```
1️⃣ 先找最具体的规则:
   Niche Deep-Dive + profile + @elsaspeak
   ↓
   找到了？→ 使用这个规则 ✅
   没找到？→ 继续往下找

2️⃣ 再找中等具体的规则:
   Niche Deep-Dive + profile
   ↓
   找到了？→ 使用这个规则 ✅
   没找到？→ 继续往下找

3️⃣ 最后找通用规则:
   Niche Deep-Dive
   ↓
   找到了？→ 使用这个规则 ✅
   没找到？→ 不过滤，保存所有内容 ⚠️
```

**实际例子**:

假设你的 Filter_Rules 表有这些规则：

| 规则 | monitoring_strategy | target_type | target_value | min_likes | min_views |
|------|---------------------|-------------|--------------|-----------|-----------|
| A | Niche Deep-Dive | profile | @elsaspeak | 500 | 5000 |
| B | Niche Deep-Dive | profile | *(空)* | 1000 | 10000 |
| C | Niche Deep-Dive | *(空)* | *(空)* | 2000 | 20000 |

当目标是 `@elsaspeak` (profile, Niche Deep-Dive):
- 查找层级 3: Niche Deep-Dive + profile + @elsaspeak → **找到规则 A** ✅
- 使用规则 A 的阈值（最具体）

当目标是 `@notionhq` (profile, Niche Deep-Dive):
- 查找层级 3: Niche Deep-Dive + profile + @notionhq → 没有
- 查找层级 2: Niche Deep-Dive + profile → **找到规则 B** ✅
- 使用规则 B 的阈值（通用于所有 profile）

当目标是 `#book` (hashtag, Niche Deep-Dive):
- 查找层级 3: Niche Deep-Dive + hashtag + #book → 没有
- 查找层级 2: Niche Deep-Dive + hashtag → 没有
- 查找层级 1: Niche Deep-Dive → **找到规则 C** ✅
- 使用规则 C 的阈值（兜底规则）

**层级匹配的好处**:

✅ **灵活性**: 可以为特定目标设置专属规则
✅ **简化管理**: 大部分目标用通用规则，特殊目标单独配置
✅ **易于维护**: 修改一条通用规则，影响所有使用它的目标

### 💡 配置技巧

**建议的规则层次**:
1. 先设置**层级 2 规则**（策略 + 类型）作为基础
   - 例如: "Niche Deep-Dive + profile" 适用于所有细分领域账号
2. 如果某个目标需要特殊对待，再添加**层级 3 规则**
   - 例如: "@elsaspeak" 是重点关注账号，设置更低阈值
3. **层级 1 规则**（只有策略）作为兜底
   - 防止漏配导致内容不被过滤

**什么时候需要层级 3 规则？**

根据目标的实际情况，灵活调整过滤标准：

**场景 1: 小体量目标 → 降低标准**
- 问题: `@blinkist` 在竞品中发布频率低，用通用规则会过滤掉大部分内容
- 解决: 添加专属规则 `Competitor Intelligence + profile + @blinkist`
  - 设置更低阈值: `min_likes = 100, min_views = 5000`
  - 确保不错过他们的任何更新

**场景 2: 大体量目标 → 提高标准**
- 问题: `@cluely` 在 Niche Deep-Dive 中内容量太大，噪音多
- 解决: 添加专属规则 `Niche Deep-Dive + profile + @cluely`
  - 设置更高阈值: `min_likes = 3000, min_views = 20000`
  - 只保留他们最受欢迎的内容

**核心思路**: 通用规则管大多数，特殊规则管例外。

---

### 🎯 阈值调整指南

**如果过滤太严格（错过好内容）**:
- 降低 `min_likes` 和 `min_views`
- 例如: 3000 → 2000, 50000 → 30000

**如果过滤太宽松（太多垃圾内容）**:
- 提高 `min_likes` 和 `min_views`
- 例如: 1000 → 2000, 10000 → 20000

**查看过滤效果**:
- 运行系统后，查看日志输出
- 示例: `✅ Scraped 30 items → Filtered to 16 items (46.7% filtered out)`
- 如果过滤率太高（>70%）→ 阈值太严格
- 如果过滤率太低（<20%）→ 阈值太宽松

### ⚠️ 重要提示

**没有匹配规则时**:
- 系统会保存**所有**抓取的内容（fail-open 设计）
- 这是为了防止配置错误导致数据丢失
- **建议**: 为每个监控策略至少配置一条规则

**确保所有目标都有策略**:
- 如果 `Monitoring_Targets` 表中的目标没有设置 `monitoring_strategy`
- 该目标的内容**不会被过滤**，所有内容都会保存
- **建议**: 检查所有活跃目标都设置了策略

---

## 📊 表格 3: TikTok_Content (内容结果)

### 作用
查看系统收集的 TikTok 内容和 AI 分析结果。

### 表格设计逻辑

**为什么字段这么多？**

这个表格需要满足 3 种不同的使用需求：

**1️⃣ 快速筛选** (基础信息)
- `author_username`: 按创作者分组
- `monitoring_strategy`: 按策略筛选（看竞品 vs 看创作策略）
- `Target`: 追溯到原始监控目标

**2️⃣ 质量判断** (互动数据)
- `likes`, `views`, `engagement_rate`: 判断内容热度
- 高互动 = 值得深入研究

**3️⃣ 洞察提取** (AI 分析)
- `strategic_score`: 快速定位最有价值的内容（7-10分优先看）
- `strategic_insights`: 直接给出关键发现（不用自己看视频总结）
- `content_type` / `niche_category`: 分类归档，方便横向对比

**为什么 AI 分析字段不统一？**

不同策略关注点不同，强制统一会导致字段冗余：

| 策略 | 特有字段 | 为什么需要 |
|------|---------|-----------|
| Competitor Intelligence | `content_type`<br>`strategic_score` | 需要快速分类（产品演示 vs 用户评价）<br>需要优先级排序（哪些最值得研究）|
| Niche Deep-Dive | `niche_category`<br>`strategic_insights` | 需要按领域分组（书籍 vs 播客 vs 生产力）<br>需要提取可复用的创作技巧 |

**设计原则**:
- ✅ 共性字段（基础+互动）→ 所有内容都有
- ✅ 策略特有字段 → 只在相关策略下填充
- ✅ 避免字段膨胀 → 不为了"统一"而添加无用字段

### 内容如何产生

**系统运行流程**:
```
1. 从 Monitoring_Targets 读取活跃目标
2. 使用 Apify 从 TikTok 抓取内容
3. 应用 Filter_Rules 过滤低质量内容
4. 保存通过过滤的内容到 TikTok_Content
5. AI 分析内容（根据 monitoring_strategy 使用不同提示词）
6. 更新分析结果到 TikTok_Content
```

**你会看到**: 已经过滤和分析的高质量内容

### 字段说明

#### 📌 基础信息

| 字段 | 内容 | 如何使用 |
|------|------|----------|
| **content_id** | TikTok 视频 ID | 唯一标识，不会重复 |
| **video_url** | 视频链接 | 点击直接观看 TikTok 视频 |
| **author_username** | 作者账号 | 谁发布的这个视频 |
| **caption** | 视频描述 | 视频的文字说明 |

#### 📈 互动数据

| 字段 | 内容 | 说明 |
|------|------|------|
| **likes** | 点赞数 | 多少人点赞 |
| **comments** | 评论数 | 多少人评论 |
| **views** | 播放量 | 多少人观看 |
| **engagement_rate** | 互动率(%) | 计算公式: (点赞 + 评论) / 播放量 × 100 |

**互动率说明**:
- 1-2%: 一般
- 3-5%: 良好
- 5%+: 优秀
- 10%+: 非常优秀（病毒式传播）

#### 🤖 AI 分析结果（根据监控策略不同）

##### 策略 1: Competitor Intelligence (竞争对手情报)

| 字段 | 内容 | 如何使用 |
|------|------|----------|
| **Analysis** | 视频内容描述 | 快速了解视频讲了什么 |
| **strategic_score** | 战略价值评分 (0-10) | **重点**: 数字越高，这个内容对我们越有价值 |
| **content_type** | 内容类型 | 分类，例如 "Product Demo", "Customer Testimonial" |
| **strategic_insights** | 战略洞察 | **最重要**: 1-3 条编号的关键发现 |

**content_type 分类** (9 种):
- Product Demo: 产品演示
- Feature Highlight: 功能亮点
- User Experience: 用户体验
- Customer Testimonial: 用户评价
- Educational Content: 教育内容
- Brand Storytelling: 品牌故事
- Promotional: 促销活动
- Behind-the-Scenes: 幕后花絮
- Other: 其他

**如何使用**:
1. 按 `strategic_score` 降序排序，查看最有价值的洞察
2. 阅读 `strategic_insights` 获取关键发现
3. 点击 `video_url` 观看原视频验证

**示例**:
```
strategic_score: 8
content_type: Feature Highlight
strategic_insights:
1. **功能展示**: Blinkist 用 15 秒快速演示"一天读完一本书"功能
2. **痛点共鸣**: 强调"没时间读书"的普遍痛点
3. **可借鉴**: 快速功能演示 + 痛点共鸣的组合很有效
```

---

##### 策略 2: Niche Deep-Dive (细分领域深度学习)

| 字段 | 内容 | 如何使用 |
|------|------|----------|
| **Analysis** | 视频内容描述 | 快速了解视频讲了什么 |
| **niche_category** | 细分类别 | AI 自动分类，方便筛选 |
| **strategic_insights** | 内容策略洞察 | **最重要**: 可以学习的内容创作技巧 |

**niche_category 分类** (7 种):
- Books & Reading: 书籍与阅读
- Podcasts & Audio Learning: 播客与音频学习
- Productivity & Habits: 生产力与习惯
- AI in Education: AI 教育应用
- Upskilling & Career: 技能提升与职业发展
- Knowledge Management: 知识管理
- Other: 其他

**如何使用**:
1. 在表格中按 `niche_category` 分组查看
2. 阅读 `strategic_insights` 学习内容策略
3. 观察不同类别的创作技巧有什么共同点

**示例**:
```
niche_category: Books & Reading
strategic_insights:
1. **开头**: 用 "POV" 格式建立代入感（"POV: 你想读书但太忙"）
2. **格式**: 快节奏剪辑 + 字幕，保持观众注意力
3. **互动**: 结尾提问鼓励评论（"你最想读哪本书？"）
```

---

#### 🔗 系统字段

| 字段 | 内容 | 说明 |
|------|------|------|
| **Target** | 链接到监控目标 | 显示这个内容来自哪个监控目标 |
| **monitoring_strategy** | 监控策略 | 自动从 Target 继承，用于 AI 分析路由 |

### 🔎 如何使用这个表格

#### 查看竞争对手洞察
1. 点击表格顶部切换到 "Competitor Intelligence" 视图
2. 按 `strategic_score` 降序排序
3. 重点阅读高分内容的 `strategic_insights`
4. 点击 `video_url` 观看原视频

#### 学习内容创作策略
1. 点击表格顶部切换到 "Niche Deep Dive" 视图
2. 按 `niche_category` 分组
3. 查看每个类别的 `strategic_insights`
4. 总结可以应用到 AI/教育领域的技巧

#### 按创作者查看
1. 在表格中展开侧边栏分组
2. 选择按 `author_username` 分组
3. 查看特定创作者的所有内容

#### 导出数据
1. 使用 Lark 的导出功能
2. 导出为 Excel 用于制作报告或进一步分析

---

## 🔄 常见工作流程

### 工作流程 1: 添加新的竞争对手监控

**目标**: 追踪新的竞争对手产品和营销策略

**步骤**:
1. 打开 `Monitoring_Targets` 表格
2. 添加新行:
   - target_value: `@新竞品账号`
   - target_type: `profile`
   - monitoring_strategy: `Competitor Intelligence`
   - active: ✓
   - results_limit: `30`
3. 检查 `Filter_Rules` 是否有对应规则（规则 1）
4. 等待系统运行（通常每天/每周运行）
5. 在 `TikTok_Content` 查看结果

---

### 工作流程 2: 学习某个话题的内容策略

**目标**: 了解某个话题（如 #productivity）的爆款内容

**步骤**:
1. 打开 `Monitoring_Targets` 表格
2. 添加新行:
   - target_value: `#productivity`
   - target_type: `hashtag`
   - monitoring_strategy: `Niche Deep-Dive`
   - active: ✓
   - results_limit: `50`
3. 打开 `Filter_Rules` 表格
4. 确认有规则 2（Niche Deep-Dive + hashtag）
5. 如果内容太多，考虑提高 `min_likes` 阈值
6. 在 `TikTok_Content` 查看结果
7. 按 `niche_category` 分组，查看内容策略

---

### 工作流程 3: 调整过滤规则

**问题**: 收到太多低质量内容

**步骤**:
1. 查看系统日志，确认过滤率（例如: "30 scraped → 25 saved, 16.7% filtered"）
2. 过滤率太低 → 需要提高阈值
3. 打开 `Filter_Rules` 表格
4. 找到对应的规则
5. 提高 `min_likes` 或 `min_views`
   - 例如: 1000 → 2000, 10000 → 20000
6. 等待下次运行，观察效果

**问题**: 错过了一些好内容

**步骤**:
1. 查看系统日志，确认过滤率（例如: "30 scraped → 8 saved, 73.3% filtered"）
2. 过滤率太高 → 阈值太严格
3. 打开 `Filter_Rules` 表格
4. 降低 `min_likes` 或 `min_views`
   - 例如: 3000 → 2000, 50000 → 30000
5. 等待下次运行，观察效果

---

## ❓ 常见问题

### Q1: 我添加了目标，但没有看到内容

**可能原因**:
1. **active 没有勾选** → 检查目标的 `active` 字段
2. **系统还没运行** → 系统通常定期运行（每天/每周），需要等待
3. **内容被过滤掉了** → 检查过滤规则是否太严格
4. **目标账号/标签没有新内容** → 检查 TikTok 上是否有新视频

**解决方法**:
- 检查 `active` 是否勾选
- 查看系统日志确认是否运行
- 临时降低过滤阈值测试

---

### Q2: 过滤规则太严格，错过好内容

**症状**: 过滤率很高（>70%），但有些内容确实不错

**解决方法**:
1. 打开 `Filter_Rules` 找到对应规则
2. 降低阈值:
   - `min_likes`: 3000 → 2000 → 1500
   - `min_views`: 50000 → 30000 → 20000
3. 保存后等待下次运行
4. 观察效果，逐步调整到合适值

**建议**:
- 账号监控: 较低阈值（不想错过竞品内容）
- 标签监控: 较高阈值（过滤大量垃圾内容）

---

### Q3: 过滤规则太宽松，太多垃圾内容

**症状**: 过滤率很低（<20%），很多低质量内容

**解决方法**:
1. 打开 `Filter_Rules` 找到对应规则
2. 提高阈值:
   - `min_likes`: 1000 → 2000 → 3000
   - `min_views`: 10000 → 20000 → 30000
3. 保存后等待下次运行
4. 观察效果，逐步调整

**目标**:
- 理想过滤率: 30-50%（保留高质量内容，过滤低质量）

---

### Q4: 应该用哪个监控策略？

**判断标准**:

| 监控对象 | 策略 | 原因 |
|----------|------|------|
| 直接竞品 (Blinkist, Headway) | Competitor Intelligence | 需要产品和营销洞察 |
| 相关工具 (Notion, Character.ai) | Niche Deep-Dive | 学习内容创作策略 |
| 话题标签 (#book, #productivity) | Niche Deep-Dive | 学习该领域的内容技巧 |
| 不确定 | Niche Deep-Dive | 更通用的分析方式 |

---

### Q5: 系统多久运行一次？

**运行频率**: 根据项目配置，通常是:
- 每天运行一次
- 或每周运行一次

**手动运行**: 开发人员可以通过命令行手动运行:
```bash
python3 src/monitor.py
```

---

### Q6: 可以修改已添加的目标吗？

**可以**，直接在 Lark Base 中修改:
- 修改 `results_limit`、`team_notes` 等字段
- 勾选/取消 `active` 来启用/停用监控
- 下次系统运行时会使用新配置

**不建议修改**:
- `target_value`, `target_type`, `monitoring_strategy`
- 如果需要改，建议添加新目标，停用旧目标

---

### Q7: 如何找到最有价值的内容？

**竞争对手内容**:
1. 打开 `TikTok_Content` 表格
2. 筛选 `monitoring_strategy = Competitor Intelligence`
3. 按 `strategic_score` 降序排序
4. 重点查看分数 7-10 的内容

**内容策略学习**:
1. 打开 `TikTok_Content` 表格
2. 筛选 `monitoring_strategy = Niche Deep-Dive`
3. 按 `niche_category` 分组
4. 阅读每个分类的 `strategic_insights`

---

## 📚 附录: 字段快速参考

### Monitoring_Targets 字段总结

| 字段 | 类型 | 必填 | 示例 |
|------|------|------|------|
| target_value | 文本 | ✓ | @blinkist 或 #book |
| platform | 单选 | ✓ | tiktok |
| target_type | 单选 | ✓ | profile 或 hashtag |
| monitoring_strategy | 单选 | ✓ | Competitor Intelligence 或 Niche Deep-Dive |
| active | 复选框 | ✓ | ✓ |
| results_limit | 数字 | ✓ | 30 |
| team_notes | 文本 | - | 备注说明 |

### Filter_Rules 字段总结

| 字段 | 类型 | 必填 | 示例 |
|------|------|------|------|
| monitoring_strategy | 单选 | ✓ | Competitor Intelligence |
| target_type | 单选 | - | profile 或 hashtag |
| target_value | 文本 | - | @blinkist (通常留空) |
| min_likes | 数字 | - | 1000 |
| min_views | 数字 | - | 10000 |
| min_engagement_rate | 数字 | - | 2.5 |
| max_age_days | 数字 | - | 30 |
| active | 复选框 | ✓ | ✓ |

### TikTok_Content 字段总结

**基础字段**:
- content_id, video_url, author_username, caption

**互动数据**:
- likes, comments, views, engagement_rate

**AI 分析 (Competitor Intelligence)**:
- Analysis, strategic_score, content_type, strategic_insights

**AI 分析 (Niche Deep-Dive)**:
- Analysis, niche_category, strategic_insights

**系统字段**:
- Target (链接), monitoring_strategy (自动继承)

---

## 🎯 快速上手清单

完成以下步骤，开始使用 AIbrary:

- [ ] 添加第一个竞争对手到 `Monitoring_Targets`
- [ ] 设置对应的过滤规则到 `Filter_Rules`
- [ ] 等待系统运行（或联系开发人员手动运行）
- [ ] 在 `TikTok_Content` 查看结果
- [ ] 根据过滤率调整规则阈值
- [ ] 添加更多监控目标

---

**需要帮助？** 联系开发人员: Leo Wu (leowu86868@gmail.com)

**最后更新**: 2025-10-31 | **版本**: 1.0
