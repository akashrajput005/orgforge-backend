from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

from app.core.security import decode_access_token
from app.db.client import get_master_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/login")


async def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    admin_id = payload.get("sub")
    if not admin_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    db = get_master_db()
    admin = await db.admins.find_one({"_id": ObjectId(admin_id)})

    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")

    return {
        "id": str(admin["_id"]),
        "email": admin["email"],
        "org_id": str(admin["org_id"]),
        "role": admin.get("role", "admin"),
    }
