from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schema.operational import (
    ServiceScheduleCreate, ServiceScheduleUpdate, ServiceScheduleOut,
    ServiceHistoryCreate, ServiceHistoryUpdate, ServiceHistoryOut,
)
from app.service.operational import (
    create_service_schedule,
    get_all_service_schedules,
    get_service_schedule_by_id,
    update_service_schedule,
    delete_service_schedule,
    create_service_history,
    get_all_service_histories,
    get_service_history_by_id,
    update_service_history,
    delete_service_history,
)

router = APIRouter(prefix="/service-schedules", tags=["service-schedules"])


# ── ServiceSchedule ───────────────────────────────────────────────────────────

@router.post("/", response_model=ServiceScheduleOut)
async def create(data: ServiceScheduleCreate, db: AsyncSession = Depends(get_db)):
    return await create_service_schedule(db=db, data=data)


@router.get("/", response_model=List[ServiceScheduleOut])
async def all_schedules(db: AsyncSession = Depends(get_db)):
    return await get_all_service_schedules(db)


@router.get("/{id}", response_model=ServiceScheduleOut)
async def schedule_by_id(id: int, db: AsyncSession = Depends(get_db)):
    schedule = await get_service_schedule_by_id(db, id)
    if not schedule:
        raise HTTPException(status_code=404, detail="ServiceSchedule not found")
    return schedule


@router.put("/{id}", response_model=ServiceScheduleOut)
async def update(id: int, data: ServiceScheduleUpdate, db: AsyncSession = Depends(get_db)):
    schedule = await update_service_schedule(db, id, data)
    if not schedule:
        raise HTTPException(status_code=404, detail="ServiceSchedule not found")
    return schedule


@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_service_schedule(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="ServiceSchedule not found")
    return {"message": "ServiceSchedule deleted"}


# ── ServiceHistory (nested under schedule) ────────────────────────────────────

@router.post("/{schedule_id}/histories", response_model=ServiceHistoryOut)
async def add_history(
    schedule_id: int,
    data: ServiceHistoryCreate,
    db: AsyncSession = Depends(get_db),
):
    schedule = await get_service_schedule_by_id(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="ServiceSchedule not found")
    return await create_service_history(db=db, data=data)


@router.get("/{schedule_id}/histories", response_model=List[ServiceHistoryOut])
async def histories_by_schedule(schedule_id: int, db: AsyncSession = Depends(get_db)):
    schedule = await get_service_schedule_by_id(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="ServiceSchedule not found")
    return schedule.history


@router.get("/{schedule_id}/histories/{history_id}", response_model=ServiceHistoryOut)
async def history_by_id(
    schedule_id: int,
    history_id: int,
    db: AsyncSession = Depends(get_db),
):
    history = await get_service_history_by_id(db, history_id)
    if not history or history.service_schedule_id != schedule_id:
        raise HTTPException(status_code=404, detail="ServiceHistory not found")
    return history


@router.put("/{schedule_id}/histories/{history_id}", response_model=ServiceHistoryOut)
async def update_history(
    schedule_id: int,
    history_id: int,
    data: ServiceHistoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    history = await get_service_history_by_id(db, history_id)
    if not history or history.service_schedule_id != schedule_id:
        raise HTTPException(status_code=404, detail="ServiceHistory not found")
    return await update_service_history(db, history_id, data)


@router.delete("/{schedule_id}/histories/{history_id}")
async def delete_history(
    schedule_id: int,
    history_id: int,
    db: AsyncSession = Depends(get_db),
):
    history = await get_service_history_by_id(db, history_id)
    if not history or history.service_schedule_id != schedule_id:
        raise HTTPException(status_code=404, detail="ServiceHistory not found")
    success = await delete_service_history(db, history_id)
    if not success:
        raise HTTPException(status_code=404, detail="ServiceHistory not found")
    return {"message": "ServiceHistory deleted"}
