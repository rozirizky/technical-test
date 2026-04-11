from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schema.user import RoleBase,RoleCreate,RoleOut
from app.service.role import (
    create,get_all_role,get_Role_by_id,update_role,delete_Role
)

router = APIRouter(prefix="/role", tags=["roles"])


@router.post("/", response_model=RoleOut)
async def create_role(
    role: RoleCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create(db=db, data=role)


@router.get("/", response_model=List[RoleOut])
async def all_role(
    db: AsyncSession = Depends(get_db)
):
    return await get_all_role(db)


@router.get("/{id}", response_model=RoleOut)
async def role_by_id(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    role = await get_Role_by_id(db, id)

    if not role:
        raise HTTPException(status_code=404, detail="role not found")

    return role


@router.delete("/{id}")
async def delete(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    success = await delete_Role(db, id)

    if not success:
        raise HTTPException(status_code=404, detail="role not found")

    return {"message": "role deleted"}


@router.put("/{id}", response_model=RoleOut)
async def update(
    id: int,
    data: RoleBase,
    db: AsyncSession = Depends(get_db)
):
    role = await update_role(db, id, data)

    if not role:
        raise HTTPException(status_code=404, detail="role not found")

    return role