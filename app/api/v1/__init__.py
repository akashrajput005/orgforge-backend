"""API v1 package for OrgForge application."""
from fastapi import APIRouter

from . import auth, org

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(org.router, prefix="/orgs", tags=["organizations"])
