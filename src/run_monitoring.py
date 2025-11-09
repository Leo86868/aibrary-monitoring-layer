#!/usr/bin/env python3
"""
AIbrary Monitoring System - Main Entry Point
Runs the complete monitoring pipeline (Layer 1 + Layer 2)
"""

import sys
from layer1_monitoring.orchestrator import main

if __name__ == "__main__":
    main()
