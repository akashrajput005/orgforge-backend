from datetime import datetime
from bson import ObjectId

from app.db.client import get_master_db
from app.utils.misc import slugify
from app.core.security import hash_password
from app.core.exceptions import OrgExistsException, OrgNotFoundException


async def create_organization(
    organization_name: str,
    display_name: str | None,
    email: str,
    password: str
):
    db = get_master_db()

    slug = slugify(organization_name)
    collection_name = f"org_{slug}_data"

    # Check uniqueness
    existing = await db.organizations.find_one({"name": slug})
    if existing:
        raise OrgExistsException()

    now = datetime.utcnow()

    # Create org collection (idempotent)
    collections = await db.list_collection_names()
    if collection_name not in collections:
        await db.create_collection(collection_name)

    # Insert organization
    org_doc = {
        "name": slug,
        "display_name": display_name or organization_name,
        "collection_name": collection_name,
        "status": "active",
        "created_at": now,
    }
    org_result = await db.organizations.insert_one(org_doc)

    # Insert admin user
    admin_doc = {
        "org_id": org_result.inserted_id,
        "email": email,
        "password_hash": hash_password(password),
        "role": "admin",
        "created_at": now,
    }
    admin_result = await db.admins.insert_one(admin_doc)

    # Link admin to org
    await db.organizations.update_one(
        {"_id": org_result.inserted_id},
        {"$set": {"admin_user_id": admin_result.inserted_id}},
    )

    return {
        "id": str(org_result.inserted_id),
        "name": slug,
        "display_name": org_doc["display_name"],
        "collection_name": collection_name,
        "created_at": now.isoformat() + "Z",
    }


async def get_organization_by_name(organization_name: str):
    db = get_master_db()
    slug = slugify(organization_name)

    org = await db.organizations.find_one({"name": slug})
    if not org:
        raise OrgNotFoundException()

    return {
        "id": str(org["_id"]),
        "name": org["name"],
        "display_name": org["display_name"],
        "collection_name": org["collection_name"],
        "status": org["status"],
        "created_at": org["created_at"].isoformat() + "Z",
    }


async def delete_organization(organization_name: str):
    db = get_master_db()
    slug = slugify(organization_name)

    org = await db.organizations.find_one({"name": slug})
    if not org:
        raise OrgNotFoundException()

    collection_name = org["collection_name"]

    # Drop org-specific collection
    collections = await db.list_collection_names()
    if collection_name in collections:
        await db.drop_collection(collection_name)

    # Remove admins
    await db.admins.delete_many({"org_id": org["_id"]})

    # Soft delete org
    await db.organizations.update_one(
        {"_id": org["_id"]},
        {"$set": {"status": "deleted", "deleted_at": datetime.utcnow()}},
    )

    return {"message": "Organization deleted successfully"}
