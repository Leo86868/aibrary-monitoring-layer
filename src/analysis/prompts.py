"""
AIbrary TikTok Monitoring System - AI Prompts
Prompt templates for different analysis types
"""

# Two-Stage AI Analysis for Content-First Competitor Intelligence
COMPETITOR_INTELLIGENCE_PROMPT = """
AIBRARY CONTEXT: AIbrary (aibrary.ai) is an AI-powered learning platform that transforms books into personalized podcasts and interactive learning experiences. Target audience: lifelong learners seeking flexible, book-based personal development. Key differentiator: personalized learning paths and AI-generated audio content, not just summaries.

Analyze this TikTok content using a two-stage approach:

CONTENT:
Creator: {author_username}
Caption: {caption}
Subtitles: {subtitles}
Performance: {likes} likes, {comments} comments, {views} views

STAGE 1 - OBJECTIVE CONTENT ANALYSIS:
Describe what this content is about without considering who created it. Focus on the actual topic, message, and format.

STAGE 2 - STRATEGIC COMPETITOR ANALYSIS:
Based on Stage 1 analysis, evaluate for AIbrary's competitive intelligence:

Strategic Score (0-10): How valuable is this content for AIbrary's competitive strategy? Balance topic relevance AND execution quality (hooks, format, messaging). BE CRITICAL - use the full range of scores, not just 8-10.

Scoring framework (all content already passed performance filters - focus on strategic value):
- 9-10 (Must Study): Direct competitor with exceptional execution quality + innovative tactics worth replicating + high topic relevance to book/learning space
- 7-8 (High Value): Strong topic relevance with good execution quality OR moderate relevance with exceptional execution/viral tactics
- 5-6 (Moderate): Moderate topic relevance with decent execution OR high relevance with mediocre execution quality
- 3-4 (Low Value): Low topic relevance with weak execution quality OR tangentially related with minimal actionable tactics
- 1-2 (Minimal): Barely related to learning/books with poor execution quality and minimal competitive insights
- 0 (Irrelevant): No connection to learning/productivity/books whatsoever

Execution quality factors: hook effectiveness, content structure, storytelling, educational clarity, format innovation, engagement techniques.

IMPORTANT: Reserve 9-10 for truly exceptional content combining high relevance AND quality. Most content should score 4-7.

Content Type: Choose ONE that best fits:
- book_content: Book summaries, insights, key takeaways, book-based content
- learning_feature: Platform features, tools, app functionality showcases
- educational_value: Tips, tutorials, how-tos, educational advice (non-book)
- user_story: Testimonials, user experiences, success stories, reviews
- brand_marketing: Announcements, promotions, campaigns, ads
- trend_engagement: Trending sounds/challenges, viral format participation
- community_culture: Behind-scenes, team, company culture, community
- productivity_lifestyle: Productivity, motivation, self-improvement, habits
- other: Doesn't fit above categories

Strategic Insights: Provide EXACTLY 2-3 numbered insights about what AIbrary can learn from this content. Each insight should cover a DIFFERENT aspect (e.g., first: what works/why, second: format/audience/messaging, third: actionable takeaway). Focus on what's genuinely interesting for THIS specific content - could be messaging, format, audience targeting, content structure, performance patterns, competitor strategy, etc. Be specific and varied.

FORMAT YOUR RESPONSE EXACTLY:

**STAGE 1 - Content Analysis:**
[Objective description of what the content is about]

**STAGE 2 - Strategic Analysis:**

**Strategic Score (0-10):** [number]

**Content Type:** [category]

**Strategic Insights:**
1. [First insight]
2. [Second insight]
3. [Third insight - optional but encouraged]
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
