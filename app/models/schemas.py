from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class OrgCreate(BaseModel):
    organization_name: str = Field(..., min_length=3)
    display_name: Optional[str] = None
    email: EmailStr
    password: str


class OrgResponse(BaseModel):
    id: str
    name: str
    display_name: Optional[str]
    collection_name: str
    created_at: str


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
