from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.core.config import get_settings
from app.database import engine, Base
from app.api.v1 import api_router
import logging
from app.core.config import get_settings

settings = get_settings()

# ==========================================
# Configure Logging Levels
# ==========================================

# Hide SQLAlchemy verbose logs
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Hide Docling logs (unless error)
logging.getLogger('docling').setLevel(logging.WARNING)

# Hide RapidOCR download logs
logging.getLogger('rapidocr').setLevel(logging.WARNING)

# Hide HuggingFace warnings
logging.getLogger('huggingface_hub').setLevel(logging.ERROR)
logging.getLogger('transformers').setLevel(logging.ERROR)

# Keep app logs visible
logging.getLogger('app').setLevel(logging.INFO)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting Smart Recruit AI Backend...")
    logger.info(f"📦 Version: {settings.VERSION}")
    
    # Create database tables (for development only)
    # In production, use Alembic migrations
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("✅ Database tables created/verified")
    logger.info("✅ Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application...")
    await engine.dispose()
    logger.info("✅ Shutdown complete")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-Powered CV Filtering System for HR Recruitment",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    #allow_origins=settings.cors_origins,
    #allow_origins=["*"], #for test app desktop
    allow_origins=[origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """API Status Check"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
        "message": "Welcome to Smart Recruit AI - Your intelligent CV filtering system"
    }

# Health check endpoint
@app.get("/health", tags=["Root"])
async def health_check():
    """Health Check Endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
