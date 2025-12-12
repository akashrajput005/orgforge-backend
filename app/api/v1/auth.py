from fastapi import APIRouter, HTTPException

from app.models.schemas import AdminLogin, TokenResponse
from app.services.auth_service import authenticate_admin

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: AdminLogin):
    token = await authenticate_admin(payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": token, "token_type": "bearer"}
