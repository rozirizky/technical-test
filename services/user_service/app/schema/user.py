from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class RoleBase(BaseModel):
    name: str = Field(..., max_length=50)
class RoleCreate(RoleBase): pass
class RoleOut(RoleBase):
    id: int
    model_config = {"from_attributes": True}

class LocationBase(BaseModel):
    name: str = Field(..., max_length=100)
    type: str = Field(..., max_length=50)
    address: str | None = None
    region: str | None = None
class LocationCreate(LocationBase): pass
class LocationOut(LocationBase):
    id: int
    model_config = {"from_attributes": True}

class UserBase(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    role_id: int
    location_id: int | None = None
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
class UserUpdate(BaseModel):
    name: str | None = None
    location_id: int | None = None
class UserOut(UserBase):
    id: int
    created_at: datetime
    role: RoleOut
    location: LocationOut | None = None
    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
class RefreshRequest(BaseModel):
    refresh_token: str
