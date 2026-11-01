"""
Main FastAPI Application Entrypoint for KrishiMitra AI.
Agricultural Market Intelligence & Crop Price Forecasting Platform (YIP 9.0).
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.api.routes_forecast import router as forecast_router
from src.api.routes_market import router as market_router
from src.api.routes_planning import router as planning_router
from src.api.routes_admin import router as admin_router

app = FastAPI(
    title="KrishiMitra AI – Agricultural Market Intelligence & Price Forecasting API",
    description="Scientific time-series price forecasting, market arbitrage, and crop planning for Kerala farmers (YIP 9.0).",
    version="1.0.0"
)

# Enable CORS for local/cloud frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(forecast_router)
app.include_router(market_router)
app.include_router(planning_router)
app.include_router(admin_router)

# Mount web directory if it exists
web_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")
if os.path.exists(web_dir):
    app.mount("/static", StaticFiles(directory=web_dir), name="static")

@app.get("/api/v1/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app_name": "KrishiMitra AI Agricultural Market Intelligence Platform",
        "project": "Kerala Young Innovators Programme (YIP 9.0)",
        "version": "1.0.0",
        "supported_commodities": ["Arecanut", "Black Pepper", "Copra", "Banana (Nendran)", "Rubber (RSS-4)", "Cardamom"]
    }

@app.get("/", include_in_schema=False)
def serve_index():
    index_file = os.path.join(web_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "KrishiMitra AI API is active. Web UI frontend mounting in progress."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)

