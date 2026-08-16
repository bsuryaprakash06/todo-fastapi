from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

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
    return {"message": "You have a token!", "token": token}
