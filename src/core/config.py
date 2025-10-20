"""
AIbrary TikTok Monitoring System - Configuration
Environment variables and constants
"""

import os
from dotenv import load_dotenv

# Load .env from config directory
config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
env_path = os.path.join(config_dir, '.env')
load_dotenv(env_path)

# ==============================================================================
# API CREDENTIALS
# ==============================================================================

# Lark API Configuration (REQUIRED)
LARK_APP_ID = os.getenv('LARK_APP_ID')
LARK_APP_SECRET = os.getenv('LARK_APP_SECRET')
LARK_BASE_ID = os.getenv('LARK_BASE_ID')

# Apify Configuration (REQUIRED)
APIFY_TOKEN = os.getenv('APIFY_TOKEN')
TIKTOK_ACTOR_ID = os.getenv('TIKTOK_ACTOR_ID', 'GdWCkxBtKWOsKjdch')  # Default actor ID is safe to keep

# AI Configuration (REQUIRED for analysis features)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# ==============================================================================
# VALIDATION - Fail fast if required credentials are missing
# ==============================================================================

_missing_vars = []

if not LARK_APP_ID:
    _missing_vars.append('LARK_APP_ID')
if not LARK_APP_SECRET:
    _missing_vars.append('LARK_APP_SECRET')
if not LARK_BASE_ID:
    _missing_vars.append('LARK_BASE_ID')
if not APIFY_TOKEN:
    _missing_vars.append('APIFY_TOKEN')
if not GEMINI_API_KEY:
    _missing_vars.append('GEMINI_API_KEY')

if _missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(_missing_vars)}\n"
        f"Please create config/.env file from .env.example template"
    )

# ==============================================================================
# TABLE NAMES
# ==============================================================================

MONITORING_TARGETS_TABLE = 'Monitoring_Targets'
TIKTOK_CONTENT_TABLE = 'TikTok_Content'

# ==============================================================================
# PROCESSING CONFIGURATION
# ==============================================================================

DEFAULT_TIMEOUT = 600  # 10 minutes
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 1  # seconds between requests
