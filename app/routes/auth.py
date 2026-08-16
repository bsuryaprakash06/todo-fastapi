from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import SignupRequest, LoginRequest
from app.auth.supabase import supabase_client
from supabase import AuthApiError
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: SignupRequest):
    try:
        response = supabase_client.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        return response
    except AuthApiError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login")
def login(user: LoginRequest):
    try:
        response = supabase_client.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return response
    except AuthApiError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(user = Depends(get_current_user)):
    try:
        supabase_client.auth.sign_out()
        return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
