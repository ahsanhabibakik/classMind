from fastapi import APIRouter
from app.core.supabase_client import supabase

router = APIRouter()

@router.get("/")
def get_all_routines():
    response = supabase.table("routines").select("*").execute()
    return {"data": response.data}
