from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_auth_info():
    return {"message": "Auth endpoint placeholder"}
