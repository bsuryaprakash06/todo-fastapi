from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.supabase import supabase_client
from supabase import AuthApiError

router = APIRouter(prefix="/protected", tags=["Protected"])

# auto_error=False allows us to manually raise 401 instead of FastAPI's default 403
security = HTTPBearer(auto_error=False)

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )
    return credentials.credentials

@router.get("/profile")
def profile(token: str = Depends(get_token)):
    try:
        user_response = supabase_client.auth.get_user(token)
        user = user_response.user
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        return {
            "id": user.id,
            "email": user.email,
            "created_at": str(user.created_at) if hasattr(user, 'created_at') else None
        }
    except AuthApiError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
