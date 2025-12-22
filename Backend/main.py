from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from getData import router as data_router
from hr_matches import router as hr_router
from uploads import router as resume_router
from market_analysis.router import router as market_router
from ml_executor import shutdown_executor
from logging_config import setup_logging
import os
from dotenv import load_dotenv

# Setup logging first (before other imports that use logging)
logger = setup_logging()
load_dotenv()

app = FastAPI(
    title="Resume Analyzer API",
    description="Production-grade Resume Analysis API",
    version="1.0.0"
)

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Starting Resume Analyzer Backend...")
    try:
        # Database singleton will initialize on first import, but let's test it
        from database import _db_singleton
        _db_singleton.client.admin.command('ping')
        logger.info("✅ Database connection initialized and tested")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    logger.info("✅ ML ThreadPoolExecutor ready")
    logger.info("✅ Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down application...")
    try:
        shutdown_executor()
        from database import _db_singleton
        _db_singleton.close()
        logger.info("✅ Shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

@app.get("/")
async def root():
    return {"message": "Resume Analyzer Backend is running!"}

@app.get("/health")
async def health_check():
    try:
        from database import _db_singleton
        # Test database connection
        _db_singleton.client.admin.command('ping')
        db_status = "connected"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "message": "Backend is operational",
        "database": db_status,
        "jwt_secret_configured": bool(os.getenv("JWT_SECRET"))
    }

app.include_router(auth_router, prefix="/auth")
app.include_router(resume_router, prefix="/resume")
app.include_router(data_router, prefix="/getme")
app.include_router(hr_router, prefix="/hr")
app.include_router(market_router, prefix="/market")
