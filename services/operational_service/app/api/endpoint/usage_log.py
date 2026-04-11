from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schema.operational import UsageLogCreate, UsageLogUpdate, UsageLogOut
from app.service.operational import (
    create_usage_log,
    get_all_usage_logs,
    get_usage_log_by_id,
    update_usage_log,
    delete_usage_log,
)

router = APIRouter(prefix="/usage-logs", tags=["usage-logs"])


@router.post("/", response_model=UsageLogOut)
async def create(data: UsageLogCreate, db: AsyncSession = Depends(get_db)):
    return await create_usage_log(db=db, data=data)


@router.get("/", response_model=List[UsageLogOut])
async def all_usage_logs(db: AsyncSession = Depends(get_db)):
    return await get_all_usage_logs(db)


@router.get("/{id}", response_model=UsageLogOut)
async def usage_log_by_id(id: int, db: AsyncSession = Depends(get_db)):
    log = await get_usage_log_by_id(db, id)
    if not log:
        raise HTTPException(status_code=404, detail="UsageLog not found")
    return log


@router.put("/{id}", response_model=UsageLogOut)
async def update(id: int, data: UsageLogUpdate, db: AsyncSession = Depends(get_db)):
    log = await update_usage_log(db, id, data)
    if not log:
        raise HTTPException(status_code=404, detail="UsageLog not found")
    return log


@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_usage_log(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="UsageLog not found")
    return {"message": "UsageLog deleted"}
