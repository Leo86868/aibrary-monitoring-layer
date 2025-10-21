#!/usr/bin/env python3
"""
Prompt Testing & Refinement Script

Purpose: Test different AI prompts without modifying production code
Usage: Edit the TEST_PROMPT below, run script, review results
"""

import sys
sys.path.insert(0, 'src')

from storage import LarkClient
from analysis import VideoAnalyzer
from core import TikTokContent, TIKTOK_CONTENT_TABLE
import google.generativeai as genai
from core import GEMINI_API_KEY

# ==============================================================================
# TEST PROMPT - EDIT THIS TO TEST DIFFERENT PROMPTS
# ==============================================================================

TEST_PROMPT = """
CONTEXT: AIbrary (aibrary.ai) is an AI-powered learning platform that turns books into personalized podcasts and interactive learning experiences. Target audience: lifelong learners seeking flexible book-based personal development.

Analyze this TikTok content in two stages:

CONTENT:
Creator: {author_username}
Caption: {caption}
Subtitles: {subtitles}
Performance: {likes:,} likes | {comments:,} comments | {views:,} views

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

**Strategic Insights:** Write 2-3 numbered insights about MARKETING/CONTENT tactics (not product features). Each insight: what technique → why it works → what AIbrary could test in their TikTok marketing. Keep it brief and direct - no bold headers, no long explanations of what the video did.

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
1. [First insight]
2. [Second insight]
3. [Third insight - include if there's a third distinct angle worth noting]
"""

# ==============================================================================
# TESTING LOGIC
# ==============================================================================

def test_prompt_with_real_data():
    """Test the prompt with real TikTok content from database"""

    print("=" * 70)
    print("🧪 PROMPT TESTING & REFINEMENT")
    print("=" * 70)

    # Initialize
    lark = LarkClient()
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # Fetch content from database
    print("\n📋 Fetching content from database...")
    table_id = lark._get_table_id(TIKTOK_CONTENT_TABLE)
    path = f"/bitable/v1/apps/{lark.base_id}/tables/{table_id}/records"
    data = lark._make_request("GET", path)

    if not data.get('items'):
        print("❌ No content in database. Run Phase 2 first.")
        return

    # Test with second record
    item = data['items'][1]
    fields = item['fields']

    content = TikTokContent(
        content_id=str(fields.get('content_id', '')),
        target_value='@openai',
        video_url=fields.get('video_url', {}).get('link', ''),
        author_username=fields.get('author_username', ''),
        caption=fields.get('caption', ''),
        likes=int(fields.get('likes', 0)),
        comments=int(fields.get('comments', 0)),
        views=int(fields.get('views', 0)),
        engagement_rate=float(fields.get('engagement_rate', 0)),
        video_download_url=fields.get('video_downlaod_url', {}).get('link', '')
    )

    print(f"   Testing with: {content.content_id}")
    print(f"   Caption: {content.caption[:80]}...")

    # Download video if available
    print("\n📥 Downloading video...")
    from analysis.video_analyzer import VideoAnalyzer
    analyzer = VideoAnalyzer()

    video_file = None
    if content.video_download_url:
        video_file = analyzer._download_video(content.video_download_url, content.content_id)
        if video_file:
            print(f"   ✅ Video downloaded")
        else:
            print(f"   ⚠️ Video download failed, using text-only")

    # Format prompt
    prompt_text = TEST_PROMPT.format(
        author_username=content.author_username,
        caption=content.caption,
        subtitles="No subtitles available",
        likes=content.likes,
        comments=content.comments,
        views=content.views
    )

    # Add video context if available
    if video_file:
        prompt_text = f"""You are analyzing a TikTok VIDEO (visual + audio content).

Pay attention to:
- Visual presentation and editing style
- On-screen text and graphics
- Speaker delivery and energy
- Production quality and professionalism

{prompt_text}"""

    # Run analysis
    print("\n🤖 Running AI analysis with TEST PROMPT...")
    print("   (This may take 60-90 seconds with video)")

    try:
        if video_file:
            with open(video_file, 'rb') as f:
                video_data = f.read()
            video_part = {"mime_type": "video/mp4", "data": video_data}
            response = model.generate_content([video_part, prompt_text])
        else:
            response = model.generate_content(prompt_text)

        # Show results
        print("\n" + "=" * 70)
        print("📊 ANALYSIS RESULTS")
        print("=" * 70)
        print(response.text)
        print("=" * 70)

        # Cleanup
        if video_file:
            import os
            if os.path.exists(video_file):
                os.remove(video_file)
                print("\n🗑️ Cleaned up video file")

        print("\n✅ Test complete!")
        print("\nNext steps:")
        print("1. Review the output above")
        print("2. Edit TEST_PROMPT in this script if needed")
        print("3. Run again to test changes")
        print("4. Once satisfied, update src/analysis/prompts.py")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        test_prompt_with_real_data()
    except Exception as e:
        print(f"\n❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
