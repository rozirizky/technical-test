from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schema.booking import (
    BookingCreate, BookingUpdate, BookingOut,
    ApprovalCreate, ApprovalUpdate, ApprovalOut,
)
from app.service.booking import (
    create_booking,
    get_all_bookings,
    get_booking_by_id,
    update_booking,
    delete_booking,
    create_approval,
    get_approvals_by_booking,
    get_approval_by_id,
    update_approval,
    delete_approval,
)

router = APIRouter(prefix="/bookings", tags=["bookings"])




@router.post("/", response_model=BookingOut)
async def create(
    data: BookingCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_booking(db=db, data=data)


@router.get("/", response_model=List[BookingOut])
async def all_bookings(
    db: AsyncSession = Depends(get_db),
):
    return await get_all_bookings(db)


@router.get("/{id}", response_model=BookingOut)
async def booking_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    booking = await get_booking_by_id(db, id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/{id}", response_model=BookingOut)
async def update(
    id: int,
    data: BookingUpdate,
    db: AsyncSession = Depends(get_db),
):
    booking = await update_booking(db, id, data)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.delete("/{id}")
async def delete(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    success = await delete_booking(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted"}




@router.post("/{booking_id}/approvals", response_model=ApprovalOut)
async def add_approval(
    booking_id: int,
    data: ApprovalCreate,
    db: AsyncSession = Depends(get_db),
):
    booking = await get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return await create_approval(db=db, booking_id=booking_id, data=data)


@router.get("/{booking_id}/approvals", response_model=List[ApprovalOut])
async def approvals_by_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
):
    booking = await get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return await get_approvals_by_booking(db, booking_id)


@router.get("/{booking_id}/approvals/{approval_id}", response_model=ApprovalOut)
async def approval_by_id(
    booking_id: int,
    approval_id: int,
    db: AsyncSession = Depends(get_db),
):
    approval = await get_approval_by_id(db, approval_id)
    if not approval or approval.booking_id != booking_id:
        raise HTTPException(status_code=404, detail="Approval not found")
    return approval


@router.put("/{booking_id}/approvals/{approval_id}", response_model=ApprovalOut)
async def update_approval_endpoint(
    booking_id: int,
    approval_id: int,
    data: ApprovalUpdate,
    db: AsyncSession = Depends(get_db),
):
    approval = await get_approval_by_id(db, approval_id)
    if not approval or approval.booking_id != booking_id:
        raise HTTPException(status_code=404, detail="Approval not found")
    return await update_approval(db, approval_id, data)


@router.delete("/{booking_id}/approvals/{approval_id}")
async def delete_approval_endpoint(
    booking_id: int,
    approval_id: int,
    db: AsyncSession = Depends(get_db),
):
    approval = await get_approval_by_id(db, approval_id)
    if not approval or approval.booking_id != booking_id:
        raise HTTPException(status_code=404, detail="Approval not found")
    success = await delete_approval(db, approval_id)
    if not success:
        raise HTTPException(status_code=404, detail="Approval not found")
    return {"message": "Approval deleted"}
