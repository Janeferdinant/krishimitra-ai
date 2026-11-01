"""
Vercel Serverless Function Entrypoint for KrishiMitra AI API.
"""

import os
import sys

# Add repository root to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.api.main import app

# Vercel serverless ASGI handler
app = app
