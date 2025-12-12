from fastapi import FastAPI

from app.api.v1.org import router as org_router
from app.api.v1.auth import router as auth_router
from app.db.client import get_client

app = FastAPI(title="OrgForge")

app.include_router(org_router)
app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    get_client()


@app.on_event("shutdown")
async def shutdown():
    get_client().close()
