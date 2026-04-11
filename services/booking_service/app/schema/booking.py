from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.models.booking import BookingStatus, ApprovalStatus


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ApprovalBase(BaseSchema):
    approver_id: int
    level: int
    status: ApprovalStatus = ApprovalStatus.pending
    notes: Optional[str] = None
    approved_at: Optional[datetime] = None


class ApprovalCreate(BaseSchema):
    approver_id: int
    level: int


class ApprovalUpdate(BaseSchema):
    status: Optional[ApprovalStatus] = None
    notes: Optional[str] = None
    approved_at: Optional[datetime] = None


class ApprovalOut(ApprovalBase):
    id: int
    booking_id: int


class BookingBase(BaseSchema):
    booking_code: str
    requester_id: int
    vehicle_id: int
    driver_id: Optional[int] = None
    departure_datetime: datetime
    return_datetime: datetime
    purpose: str
    destination: str
    passenger_count: int = 1
    status: BookingStatus = BookingStatus.draft


class BookingCreate(BaseSchema):
    booking_code: str
    requester_id: int
    vehicle_id: int
    driver_id: Optional[int] = None
    departure_datetime: datetime
    return_datetime: datetime
    purpose: str
    destination: str
    passenger_count: int = 1


class BookingUpdate(BaseSchema):
    booking_code: Optional[str] = None
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None
    departure_datetime: Optional[datetime] = None
    return_datetime: Optional[datetime] = None
    purpose: Optional[str] = None
    destination: Optional[str] = None
    passenger_count: Optional[int] = None
    status: Optional[BookingStatus] = None


class BookingOut(BookingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    approvals: List[ApprovalOut] = []
