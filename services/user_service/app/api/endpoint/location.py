from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schema.user import LocationCreate, LocationOut
from app.service.location import (
    create, get_all_locations, get_location_by_id, delete_location, update_location
)

router = APIRouter(prefix="/location", tags=["locations"])


@router.post("/", response_model=LocationOut)
async def create_location(
    location: LocationCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create(db=db, data=location)


@router.get("/", response_model=List[LocationOut])
async def all_location(
    db: AsyncSession = Depends(get_db)
):
    return await get_all_locations(db)


@router.get("/{id}", response_model=LocationOut)
async def location_by_id(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    location = await get_location_by_id(db, id)

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location


@router.delete("/{id}")
async def delete(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    success = await delete_location(db, id)

    if not success:
        raise HTTPException(status_code=404, detail="Location not found")

    return {"message": "Location deleted"}


@router.put("/{id}", response_model=LocationOut)
async def update(
    id: int,
    data: LocationCreate,
    db: AsyncSession = Depends(get_db)
):
    location = await update_location(db, id, data)

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location
