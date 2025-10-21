"""
AIbrary TikTok Monitoring System - Response Parsers
Parse AI model responses into structured data
"""

import re
from core.models import AnalysisResult


def parse_competitor_intelligence_response(content_id: str, response_text: str) -> AnalysisResult:
    """Parse two-stage AI response into AnalysisResult"""

    # Default values
    general_analysis = ""
    strategic_score = 5
    content_type = "other"
    strategic_insights = ""

    # Extract Stage 1 - General Analysis
    stage1_match = re.search(r'\*\*STAGE 1 - Content Analysis:\*\*\s*(.*?)(?=\*\*STAGE 2|$)', response_text, re.IGNORECASE | re.DOTALL)
    if stage1_match:
        general_analysis = stage1_match.group(1).strip()
    else:
        # Fallback: use first 200 chars if structure not found
        general_analysis = response_text[:200].strip()

    # Extract Stage 2 Strategic Fields

    # Strategic Score - pattern: "**Score:** 8/10"
    score_match = re.search(r'\*\*score:\*\*\s*(\d+)', response_text, re.IGNORECASE)
    if score_match:
        strategic_score = min(int(score_match.group(1)), 10)

    # Content Type - pattern: "**Content Type:** book_content"
    content_type_match = re.search(r'\*\*content type:\*\*\s*([a-zA-Z_]+)', response_text, re.IGNORECASE)
    if content_type_match:
        content_type = content_type_match.group(1).lower()

    # Strategic Insights - pattern: "**Strategic Insights:**\n1. [text]\n2. [text]"
    # Extract the entire numbered list section
    insights_match = re.search(r'\*\*strategic insights:\*\*\s*((?:\d+\..*?(?=\n\d+\.|\n\*\*|$))+)', response_text, re.IGNORECASE | re.DOTALL)
    if insights_match:
        strategic_insights = insights_match.group(1).strip()
    else:
        # Fallback: try to get any text after Strategic Insights
        fallback_match = re.search(r'\*\*strategic insights:\*\*\s*(.*?)(?=\n\*\*|$)', response_text, re.IGNORECASE | re.DOTALL)
        if fallback_match:
            strategic_insights = fallback_match.group(1).strip()

    result = AnalysisResult(
        content_id=content_id,
        general_analysis=general_analysis,
        strategic_score=strategic_score,
        content_type=content_type,
        strategic_insights=strategic_insights,
        summary=f"Strategic Score: {strategic_score}/10 | Type: {content_type}"
    )

    return result


def parse_general_analysis_response(content_id: str, response_text: str) -> AnalysisResult:
    """Parse legacy general analysis response"""

    # Simple parsing - can be enhanced with structured output
    lines = response_text.lower().split('\n')

    category = "Unknown"
    sentiment = "neutral"
    viral_score = 5

    for line in lines:
        if 'category:' in line:
            category = line.split('category:')[1].strip()
        elif 'sentiment:' in line:
            sentiment = line.split('sentiment:')[1].strip()
        elif 'viral' in line and 'score' in line:
            try:
                # Extract number from line
                numbers = re.findall(r'\d+', line)
                if numbers:
                    viral_score = min(int(numbers[0]), 10)
            except:
                pass

    result = AnalysisResult(
        content_id=content_id,
        strategic_score=viral_score,
        content_type=category,
        strategic_insights="",
        general_analysis=response_text[:500],
        summary=response_text[:500]
    )

    return result


def parse_subtitle_content(subtitle_text: str) -> str:
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


def extract_bracketed_value(line: str, default: str = "") -> str:
    """Extract value from [brackets] in a line"""
    match = re.search(r'\[(.*?)\]', line)
    if match:
        return match.group(1).strip()
    return default
