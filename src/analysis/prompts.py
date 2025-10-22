"""
AIbrary TikTok Monitoring System - AI Prompts
Prompt templates for different analysis types
"""

# Two-Stage AI Analysis for Content-First Competitor Intelligence
COMPETITOR_INTELLIGENCE_PROMPT = """
IMPORTANT: You MUST provide EXACTLY 2-3 strategic insights (not 1, not 0). This is a strict requirement.

CONTEXT: AIbrary (aibrary.ai) is an AI-powered learning platform that turns books into personalized podcasts and interactive learning experiences. Target audience: lifelong learners seeking flexible book-based personal development.

Analyze this TikTok content in two stages:

CONTENT:
Creator: {author_username}
Caption: {caption}
Subtitles: {subtitles}
Performance: {likes} likes, {comments} comments, {views} views

---

STAGE 1 - What is this content actually about?
Describe the topic, message, and format without considering the creator. Write as much as needed to capture what matters.

STAGE 2 - How useful is this for AIbrary?

**Score (0-10):** Rate based on topic relevance + how well it's done.
- 9-10: Must study - direct competitor doing something exceptional
- 7-8: High value - either highly relevant with solid delivery OR moderate relevance with standout techniques
- 5-6: Moderate - decent on both fronts or strong in one, weak in other
- 3-4: Low - tangentially related or poorly done
- 1-2: Minimal - barely relevant
- 0: Irrelevant

Be critical. Most content scores 4-7. Reserve 9-10 for truly exceptional work.

**Content Type:** Pick ONE that fits best:
book_content | learning_feature | educational_value | user_story | brand_marketing | trend_engagement | community_culture | productivity_lifestyle | other

**Strategic Insights:** Write EXACTLY 2-3 numbered insights (minimum 2, maximum 3) about MARKETING/CONTENT tactics (not product features). Each insight: what technique → why it works → what AIbrary could test in their TikTok marketing. Keep it brief and direct - no bold headers, no long explanations of what the video did.

Good examples (brief, marketing-focused):
- "States 'everything was AI-generated' upfront - builds credibility before showing results. AIbrary could try 'this entire summary was AI-personalized for you' at the start"
- "Puts humans inside AI worlds instead of narrating over them - makes tech feel tangible not abstract. AIbrary could show users 'inside' book worlds vs UI screenshots"
- "Opens with question in 3 seconds instead of title card - stops scroll via curiosity gap. AIbrary could test 'What if you could master any book in 15min?' hooks"

Bad examples (avoid these):
- "**Enhanced Sensory Experience via Sound:** Sora 2 emphasizes its new ability to generate integrated sound, dramatically elevating the realism..." (too long, bold header, describes video not marketing)
- "AIbrary could enhance book-to-podcast conversions by adding ambient soundscapes" (product feature, not marketing tactic)
- "Clear AI-generated disclosure upfront in the first few seconds" (just description, no why/try)

---

FORMAT YOUR RESPONSE:

**STAGE 1 - Content Analysis:**
[Your analysis here]

**STAGE 2 - Strategic Analysis:**

**Score:** X/10

**Content Type:** [category]

**Strategic Insights:**
1. [First insight - REQUIRED]
2. [Second insight - REQUIRED]
3. [Third insight - OPTIONAL but encouraged]

YOU MUST provide at least 2 insights. Do not stop at 1.
"""

# Niche Deep-Dive Analysis for Adjacent Niche Content Strategies
NICHE_DEEPDIVE_PROMPT = """
IMPORTANT: You MUST provide EXACTLY 2-3 strategic insights (not 1, not 0). This is a strict requirement.

CONTEXT: AIbrary (aibrary.ai) is an AI-powered learning platform that turns books into personalized podcasts and interactive learning experiences. We're analyzing adjacent niche creators (not direct competitors) to learn content strategies from podcasts, books, productivity, and learning spaces.

Analyze this TikTok content in two stages:

CONTENT:
Creator: {author_username}
Caption: {caption}
Subtitles: {subtitles}
Performance: {likes} likes, {comments} comments, {views} views

---

STAGE 1 - What is this content actually about?
Describe the topic, message, and format. Focus on the content strategy, hook type, and format style used.

STAGE 2 - Content Strategy Analysis

**Score (0-10):** Rate based on content strategy execution quality (hooks, format, storytelling, engagement tactics).
- 9-10: Exceptional - masterful content strategy worth deep study
- 7-8: Strong - effective tactics with clear learnings for AIbrary
- 5-6: Solid - decent execution with some useful elements
- 3-4: Weak - basic approach with limited takeaways
- 1-2: Poor - low-effort or ineffective strategy
- 0: No value

Be critical. Most content scores 4-7. Reserve 9-10 for truly exceptional content strategies.

**Niche Category:** Pick EXACTLY ONE category that fits best:
Podcasts & Audio Learning | Books & Reading | Productivity & Habits | AI in Education | Upskilling & Career | Knowledge Management | Other

**Strategic Insights:** Write EXACTLY 2-3 numbered insights (minimum 2, maximum 3) about CONTENT STRATEGIES and TACTICS used in this adjacent niche that AIbrary could adapt. Each insight: what tactic → why it works → how AIbrary could test it. Keep it brief and actionable.

Focus on:
- Hook types (curiosity gaps, problem statements, storytelling openings)
- Format styles (talking head vs B-roll, text overlays, visual metaphors)
- Engagement tactics (community building, challenges, user participation)
- Trending topics in this niche space

Good examples (brief, strategy-focused):
- "Opens with '3 books that changed my life' list format - creates immediate curiosity and saves time. AIbrary could test 'top 3 books for X goal' hooks targeting specific outcomes"
- "Uses text overlay to highlight key book quotes while speaking - reinforces message via dual channels. AIbrary could layer quotes over podcast visuals"
- "Creates urgency with 'reading challenge' framing - turns content consumption into a game. AIbrary could try '7-day book mastery challenge' campaigns"

Bad examples (avoid these):
- "**Enhanced Reading Experience:** This creator emphasizes the emotional impact of reading..." (too long, bold header, describes content not strategy)
- "AIbrary could add more book summaries to the platform" (product feature, not content tactic)
- "Uses good lighting and clear audio" (production quality, not content strategy)

---

FORMAT YOUR RESPONSE:

**STAGE 1 - Content Analysis:**
[Your analysis here]

**STAGE 2 - Strategic Analysis:**

**Score:** X/10

**Niche Category:** [category - must be one of the 7 options]

**Strategic Insights:**
1. [First insight - REQUIRED]
2. [Second insight - REQUIRED]
3. [Third insight - OPTIONAL but encouraged]

YOU MUST provide at least 2 insights. Do not stop at 1.
"""

# Legacy prompt for general analysis (keeping for backward compatibility)
VIDEO_ANALYSIS_PROMPT = """
Analyze this TikTok video and provide insights on:
1. Content category (educational, entertainment, product, etc.)
2. Key topics discussed
3. Sentiment (positive, negative, neutral)
4. Target audience
5. Call-to-actions if any
6. Brand mentions or product placements
7. Viral potential score (1-10)

Caption: {caption}
Subtitles: {subtitles}
"""
