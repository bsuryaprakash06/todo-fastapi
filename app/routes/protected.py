from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/profile")
def profile(user = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": str(user.created_at) if hasattr(user, 'created_at') else None
    }

@router.get("/dashboard")
def dashboard(user = Depends(get_current_user)):
    return {
        "message": f"Welcome to your dashboard, {user.email}!"
    }
