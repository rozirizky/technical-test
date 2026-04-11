from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schema.user import UserCreate, UserUpdate, UserOut
from app.service.users import (
    create,
    get_all_users,
    get_user_by_id,
    delete_user,
    update_user
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create(db=db, data=user)


@router.get("/", response_model=List[UserOut])
async def all_user(
    db: AsyncSession = Depends(get_db)
):
    return await get_all_users(db)


@router.get("/{id}", response_model=UserOut)
async def user_by_id(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    user = await get_user_by_id(db, id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/{id}")
async def delete(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    success = await delete_user(db, id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted"}


@router.put("/{id}", response_model=UserOut)
async def update(
    id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    user = await update_user(db, id, data)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user