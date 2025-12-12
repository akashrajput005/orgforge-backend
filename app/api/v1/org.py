from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import OrgCreate, OrgResponse
from app.services.org_service import (
    create_organization,
    get_organization_by_name,
    delete_organization,
)
from app.deps.auth_deps import get_current_admin

router = APIRouter(prefix="/api/v1/org", tags=["Organization"])


@router.post("/create", response_model=OrgResponse)
async def create_org(payload: OrgCreate):
    return await create_organization(
        payload.organization_name,
        payload.display_name,
        payload.email,
        payload.password,
    )


@router.get("/get")
async def get_org(organization_name: str):
    return await get_organization_by_name(organization_name)


@router.delete("/delete")
async def delete_org(
    organization_name: str,
    current_admin: dict = Depends(get_current_admin),
):
    # Ownership check
    org = await get_organization_by_name(organization_name)
    if current_admin["org_id"] != org["id"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    return await delete_organization(organization_name)
