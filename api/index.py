"""
Vercel Serverless Function Entrypoint for KrishiMitra AI API.
"""

import os
import sys

# Add repository root to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.api.main import app as fastapi_app

class VercelPathRewriteMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http":
            matched_path = None
            for k, v in scope.get("headers", []):
                if k.lower() == b"x-matched-path":
                    matched_path = v.decode("latin1")
                    break
            if matched_path and scope.get("path") in ["/api/index.py", "/api/index", "/api"]:
                scope["path"] = matched_path
                scope["raw_path"] = matched_path.encode("latin1")
        await self.app(scope, receive, send)

# Vercel serverless ASGI handler
app = VercelPathRewriteMiddleware(fastapi_app)
