from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.supabase_service import supabase

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(user: UserCreate):
    response = supabase.auth.sign_up(email=user.email, password=user.password)
    if response.user is None:
        raise HTTPException(status_code=400, detail=response.message)
    return {"message": "User created successfully", "user": response.user}

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(user: UserLogin):
    response = supabase.auth.sign_in(email=user.email, password=user.password)
    if response.session is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": response.session.access_token, "user": response.user}
