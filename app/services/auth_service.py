from bson import ObjectId

from app.db.client import get_master_db
from app.core.security import verify_password, create_access_token


async def authenticate_admin(email: str, password: str) -> str | None:
    db = get_master_db()

    admin = await db.admins.find_one({"email": email})
    if not admin:
        return None

    if not verify_password(password, admin["password_hash"]):
        return None

    token_payload = {
        "sub": str(admin["_id"]),
        "email": admin["email"],
        "org_id": str(admin["org_id"]),
        "role": admin.get("role", "admin"),
    }

    return create_access_token(token_payload)
