from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schema.operational import ServiceHistoryCreate, ServiceHistoryUpdate, ServiceHistoryOut
from app.service.operational import (
    create_service_history,
    get_all_service_histories,
    get_service_history_by_id,
    update_service_history,
    delete_service_history,
)

router = APIRouter(prefix="/service-histories", tags=["service-histories"])


@router.post("/", response_model=ServiceHistoryOut)
async def create(data: ServiceHistoryCreate, db: AsyncSession = Depends(get_db)):
    return await create_service_history(db=db, data=data)


@router.get("/", response_model=List[ServiceHistoryOut])
async def all_histories(db: AsyncSession = Depends(get_db)):
    return await get_all_service_histories(db)


@router.get("/{id}", response_model=ServiceHistoryOut)
async def history_by_id(id: int, db: AsyncSession = Depends(get_db)):
    history = await get_service_history_by_id(db, id)
    if not history:
        raise HTTPException(status_code=404, detail="ServiceHistory not found")
    return history


@router.put("/{id}", response_model=ServiceHistoryOut)
async def update(id: int, data: ServiceHistoryUpdate, db: AsyncSession = Depends(get_db)):
    history = await update_service_history(db, id, data)
    if not history:
        raise HTTPException(status_code=404, detail="ServiceHistory not found")
    return history


@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_service_history(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="ServiceHistory not found")
    return {"message": "ServiceHistory deleted"}
