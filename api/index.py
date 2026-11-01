"""
Vercel Serverless Function Entrypoint for KrishiMitra AI API.
"""

import os
import sys
import urllib.parse

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
            raw_qs = scope.get("query_string", b"").decode("latin1")
            parsed_qs = urllib.parse.parse_qs(raw_qs, keep_blank_values=True)
            
            subpath = None
            if "__path" in parsed_qs:
                subpath = parsed_qs.pop("__path")[0]
            else:
                for k, v in scope.get("headers", []):
                    if k.lower() == b"x-matched-path":
                        matched = v.decode("latin1")
                        if matched.startswith("/api/"):
                            subpath = matched[len("/api/"):]
                        break
                        
            if subpath:
                # Ensure leading slash and prefix with /api/
                clean_subpath = subpath.lstrip("/")
                new_path = f"/api/{clean_subpath}"
                scope["path"] = new_path
                scope["raw_path"] = new_path.encode("latin1")
                
                # Reconstruct query string without __path
                new_qs = urllib.parse.urlencode(parsed_qs, doseq=True)
                scope["query_string"] = new_qs.encode("latin1")
                
        await self.app(scope, receive, send)

# Vercel serverless ASGI handler
app = VercelPathRewriteMiddleware(fastapi_app)
