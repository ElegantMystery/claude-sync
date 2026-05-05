#!/usr/bin/env python3
"""CLI entry point for claude-sync plugin.

This module wraps sync.main() and ensures proper Python path setup
so that sync.py and filter.py modules can be imported correctly.
"""

import sys
from pathlib import Path

# Ensure scripts/ directory is in the Python path for imports
SCRIPT_DIR = Path(__file__).parent.resolve()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Import and delegate to sync.main
from sync import main

if __name__ == '__main__':
    sys.exit(0 if main() else 1)