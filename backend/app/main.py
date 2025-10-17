from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routines, auth, notifications
from app.core.supabase_client import supabase
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.jwt import init_jwks_client
import time

# Setup logging
setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="ClassMind Backend",
    version="1.0.0",
    description="Backend API for ClassMind - AI-powered routine management"
)

logger.info("Starting ClassMind Backend application")

# Initialize Clerk JWKS client
init_jwks_client(settings.CLERK_JWKS_URL)
logger.info("Clerk JWKS client initialized")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routines.router, prefix="/api/routines", tags=["Routines"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])

@app.get("/")
def root():
    return {"message": "🚀 ClassMind Backend is running"}

@app.get("/health", tags=["Health"])
def health():
    """Basic health check endpoint"""
    return {"status": "ok"}

@app.get("/db-health", tags=["Health"])
def db_health():
    """Health check with database connectivity test and latency measurement"""
    start_time = time.time()
    try:
        # Try to query the routines table
        res = supabase.table("routines").select("*").limit(1).execute()
        latency_ms = round((time.time() - start_time) * 1000, 2)
        
        return {
            "status": "connected",
            "database": "supabase",
            "latency_ms": latency_ms,
            "rows_sampled": len(res.data or [])
        }
    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "status": "error",
            "database": "supabase",
            "latency_ms": latency_ms,
            "details": str(e)
        }
