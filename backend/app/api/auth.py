from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    return {"message": "Login endpoint"}

@router.post("/signup")
def signup():
    return {"message": "Signup endpoint"}

@router.post("/logout")
def logout():
    return {"message": "Logout endpoint"}
