from fastapi import FastAPI
from app.api import routines, auth, notifications

app = FastAPI(title="ClassMind Backend", version="1.0.0")

app.include_router(routines.router, prefix="/api/routines", tags=["Routines"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])

@app.get("/")
def root():
    return {"message": "🚀 ClassMind Backend is running"}
