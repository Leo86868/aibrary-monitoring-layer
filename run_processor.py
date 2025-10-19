#!/usr/bin/env python3
"""
AIbrary TikTok Monitoring System - Main Entry Point
Run this script to execute the TikTok monitoring system
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from monitor import main

if __name__ == "__main__":
    main()