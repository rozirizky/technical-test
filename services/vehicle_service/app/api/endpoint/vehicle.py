from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schema.vehicle import VehicleCreate, VehicleUpdate, VehicleOut
from app.service.vehicle import (
    create,
    get_all_vehicles,
    get_vehicle_by_id,
    delete_vehicle,
    update_vehicle,
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("/", response_model=VehicleOut)
async def create_vehicle(
    vehicle: VehicleCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create(db=db, data=vehicle)


@router.get("/", response_model=List[VehicleOut])
async def all_vehicles(
    db: AsyncSession = Depends(get_db),
):
    return await get_all_vehicles(db)


@router.get("/{id}", response_model=VehicleOut)
async def vehicle_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    vehicle = await get_vehicle_by_id(db, id)

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle


@router.put("/{id}", response_model=VehicleOut)
async def update(
    id: int,
    data: VehicleUpdate,
    db: AsyncSession = Depends(get_db),
):
    vehicle = await update_vehicle(db, id, data)

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle


@router.delete("/{id}")
async def delete(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    success = await delete_vehicle(db, id)

    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return {"message": "Vehicle deleted"}
