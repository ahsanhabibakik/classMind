from fastapi import FastAPI
from app.api import routines, auth, notifications
from app.core.supabase_client import supabase

app = FastAPI(title="ClassMind Backend", version="1.0.0")

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
    """Health check with database connectivity test"""
    try:
        # Try to query the routines table
        res = supabase.table("routines").select("*").limit(1).execute()
        return {
            "status": "connected",
            "database": "supabase",
            "rows_sampled": len(res.data or [])
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "supabase",
            "details": str(e)
        }
