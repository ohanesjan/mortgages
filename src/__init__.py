# src/__init__.py

import sys
import os

# Dynamically set the path to include the src directory
src_path = os.path.abspath(os.path.dirname(__file__))
if src_path not in sys.path:
    sys.path.append(src_path)