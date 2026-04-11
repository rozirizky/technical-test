from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schema.vehicle import DriverCreate, DriverUpdate, DriverOut
from app.service.driver import (
    create,
    get_all_drivers,
    get_driver_by_id,
    delete_driver,
    update_driver,
)

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("/", response_model=DriverOut)
async def create_driver(
    driver: DriverCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create(db=db, data=driver)


@router.get("/", response_model=List[DriverOut])
async def all_drivers(
    db: AsyncSession = Depends(get_db),
):
    return await get_all_drivers(db)


@router.get("/{id}", response_model=DriverOut)
async def driver_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    driver = await get_driver_by_id(db, id)

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    return driver


@router.put("/{id}", response_model=DriverOut)
async def update(
    id: int,
    data: DriverUpdate,
    db: AsyncSession = Depends(get_db),
):
    driver = await update_driver(db, id, data)

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    return driver


@router.delete("/{id}")
async def delete(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    success = await delete_driver(db, id)

    if not success:
        raise HTTPException(status_code=404, detail="Driver not found")

    return {"message": "Driver deleted"}
