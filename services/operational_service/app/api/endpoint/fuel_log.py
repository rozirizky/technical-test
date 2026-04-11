from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schema.operational import FuelLogCreate, FuelLogUpdate, FuelLogOut
from app.service.operational import (
    create_fuel_log,
    get_all_fuel_logs,
    get_fuel_log_by_id,
    update_fuel_log,
    delete_fuel_log,
)

router = APIRouter(prefix="/fuel-logs", tags=["fuel-logs"])


@router.post("/", response_model=FuelLogOut)
async def create(data: FuelLogCreate, db: AsyncSession = Depends(get_db)):
    return await create_fuel_log(db=db, data=data)


@router.get("/", response_model=List[FuelLogOut])
async def all_fuel_logs(db: AsyncSession = Depends(get_db)):
    return await get_all_fuel_logs(db)


@router.get("/{id}", response_model=FuelLogOut)
async def fuel_log_by_id(id: int, db: AsyncSession = Depends(get_db)):
    log = await get_fuel_log_by_id(db, id)
    if not log:
        raise HTTPException(status_code=404, detail="FuelLog not found")
    return log


@router.put("/{id}", response_model=FuelLogOut)
async def update(id: int, data: FuelLogUpdate, db: AsyncSession = Depends(get_db)):
    log = await update_fuel_log(db, id, data)
    if not log:
        raise HTTPException(status_code=404, detail="FuelLog not found")
    return log


@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_fuel_log(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="FuelLog not found")
    return {"message": "FuelLog deleted"}
