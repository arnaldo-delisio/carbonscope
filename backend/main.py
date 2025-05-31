from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import products, analysis, community
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title="CarbonScope API",
    description="AI-Powered Multi-Modal Carbon Footprint Analyzer",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(community.router, prefix="/api/v1/community", tags=["community"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to CarbonScope API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "carbonscope-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
