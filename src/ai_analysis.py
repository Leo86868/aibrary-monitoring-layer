#!/usr/bin/env python3
"""
AIbrary TikTok Monitoring System - AI Analysis Module
Processes TikTok videos and subtitles for AI-powered insights
"""

import os
import requests
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import google.generativeai as genai
from core import TikTokContent, APIFY_TOKEN

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Google Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Analysis prompt templates
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

# ==============================================================================
# AI ANALYSIS ENGINE
# ==============================================================================

@dataclass
class AnalysisResult:
    """Result of AI video analysis"""
    content_id: str
    category: str
    topics: List[str]
    sentiment: str
    target_audience: str
    call_to_actions: List[str]
    brand_mentions: List[str]
    viral_score: int
    summary: str
    raw_response: str

class VideoAnalyzer:
    """Handles AI analysis of TikTok videos"""

    def __init__(self):
        """Initialize the video analyzer with API credentials"""
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            print("⚠️ GEMINI_API_KEY not found - AI analysis disabled")

    def analyze_content(self, content: TikTokContent) -> Optional[AnalysisResult]:
        """
        Analyze TikTok content using available data
        Priority: Subtitles > Video > Caption only
        """
        if not self.model:
            return None

        try:
            # Prepare analysis data
            analysis_input = self._prepare_analysis_input(content)

            # Generate analysis using Gemini
            response = self.model.generate_content(analysis_input)

            # Parse and structure the response
            result = self._parse_analysis_response(content.content_id, response.text)

            return result

        except Exception as e:
            print(f"❌ AI analysis failed for {content.content_id}: {e}")
            return None

    def _prepare_analysis_input(self, content: TikTokContent) -> str:
        """Prepare the input prompt for AI analysis"""

        # Get subtitle text if available
        subtitles = ""
        if content.subtitle_url:
            subtitles = self._fetch_subtitles(content.subtitle_url)

        # Format the analysis prompt
        prompt = VIDEO_ANALYSIS_PROMPT.format(
            caption=content.caption or "No caption provided",
            subtitles=subtitles or "No subtitles available"
        )

        # If video URL is available, we could add video analysis here
        # For now, we're focusing on text-based analysis

        return prompt

    def _fetch_subtitles(self, subtitle_url: str) -> str:
        """Fetch subtitle text from URL"""
        try:
            if subtitle_url:
                response = requests.get(subtitle_url, timeout=10)
                if response.status_code == 200:
                    # Parse subtitle format (SRT, VTT, etc.)
                    return self._parse_subtitle_content(response.text)
        except Exception as e:
            print(f"⚠️ Failed to fetch subtitles: {e}")

        return ""

    def _parse_subtitle_content(self, subtitle_text: str) -> str:
        """Parse subtitle file content to extract text"""
        # Simple extraction - can be enhanced for different formats
        lines = subtitle_text.split('\n')
        text_lines = []

        for line in lines:
            line = line.strip()
            # Skip timecodes and numbers
            if line and not line.isdigit() and '-->' not in line:
                text_lines.append(line)

        return ' '.join(text_lines)

    def _parse_analysis_response(self, content_id: str, response_text: str) -> AnalysisResult:
        """Parse AI response into structured result"""

        # Default values
        result = AnalysisResult(
            content_id=content_id,
            category="Unknown",
            topics=[],
            sentiment="neutral",
            target_audience="General",
            call_to_actions=[],
            brand_mentions=[],
            viral_score=5,
            summary=response_text[:500],  # First 500 chars as summary
            raw_response=response_text
        )

        # Simple parsing - can be enhanced with structured output
        lines = response_text.lower().split('\n')

        for line in lines:
            if 'category:' in line:
                result.category = line.split('category:')[1].strip()
            elif 'sentiment:' in line:
                result.sentiment = line.split('sentiment:')[1].strip()
            elif 'viral' in line and 'score' in line:
                try:
                    # Extract number from line
                    import re
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        result.viral_score = min(int(numbers[0]), 10)
                except:
                    pass

        return result

    def batch_analyze(self, content_list: List[TikTokContent]) -> List[AnalysisResult]:
        """Analyze multiple content items"""
        results = []

        for content in content_list:
            print(f"🤖 Analyzing content: {content.content_id}")
            result = self.analyze_content(content)
            if result:
                results.append(result)
                # Update content with analysis
                content.ai_analysis_result = result.summary
                content.video_analyzed = True

        return results

# ==============================================================================
# ANALYSIS UTILITIES
# ==============================================================================

def format_analysis_for_storage(result: AnalysisResult) -> str:
    """Format analysis result for storage in database"""

    formatted = f"""
📊 Category: {result.category}
💭 Sentiment: {result.sentiment}
🎯 Target Audience: {result.target_audience}
🔥 Viral Score: {result.viral_score}/10

📌 Topics: {', '.join(result.topics) if result.topics else 'N/A'}
📢 CTAs: {', '.join(result.call_to_actions) if result.call_to_actions else 'None'}
🏷️ Brands: {', '.join(result.brand_mentions) if result.brand_mentions else 'None'}

📝 Summary: {result.summary}
"""

    return formatted.strip()

def should_analyze_content(content: TikTokContent, min_engagement_rate: float = 5.0) -> bool:
    """
    Determine if content should be analyzed based on criteria
    Can be customized for selective processing to manage costs
    """

    # Skip if already analyzed
    if content.video_analyzed:
        return False

    # Analyze high-engagement content
    if content.engagement_rate >= min_engagement_rate:
        return True

    # Analyze if has significant views
    if content.views > 10000:
        return True

    # Skip low-engagement content to save costs
    return False

# ==============================================================================
# MAIN ANALYSIS PIPELINE
# ==============================================================================

def analyze_new_content(content_list: List[TikTokContent]) -> Dict[str, Any]:
    """
    Main entry point for analyzing new TikTok content
    Returns analysis results and statistics
    """

    analyzer = VideoAnalyzer()

    # Filter content for analysis
    to_analyze = [c for c in content_list if should_analyze_content(c)]

    print(f"🎬 Analyzing {len(to_analyze)} of {len(content_list)} content items")

    # Perform analysis
    results = analyzer.batch_analyze(to_analyze)

    # Prepare summary
    summary = {
        "total_content": len(content_list),
        "analyzed": len(results),
        "skipped": len(content_list) - len(to_analyze),
        "results": results,
        "categories": {},
        "sentiments": {},
        "avg_viral_score": 0
    }

    # Aggregate statistics
    if results:
        for result in results:
            summary["categories"][result.category] = summary["categories"].get(result.category, 0) + 1
            summary["sentiments"][result.sentiment] = summary["sentiments"].get(result.sentiment, 0) + 1

        summary["avg_viral_score"] = sum(r.viral_score for r in results) / len(results)

    return summary