from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List
from app.models.operational import ServiceStatus


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ── FuelLog ───────────────────────────────────────────────────────────────────

class FuelLogBase(BaseSchema):
    vehicle_id: int
    booking_id: Optional[int] = None
    liters: float
    odometer: float
    log_date: date


class FuelLogCreate(FuelLogBase):
    pass


class FuelLogUpdate(BaseSchema):
    vehicle_id: Optional[int] = None
    booking_id: Optional[int] = None
    liters: Optional[float] = None
    odometer: Optional[float] = None
    log_date: Optional[date] = None


class FuelLogOut(FuelLogBase):
    id: int


# ── ServiceSchedule ───────────────────────────────────────────────────────────

class ServiceScheduleBase(BaseSchema):
    vehicle_id: int
    service_type: str
    scheduled_date: date
    odometer_threshold: Optional[float] = None
    status: ServiceStatus = ServiceStatus.scheduled
    notes: Optional[str] = None


class ServiceScheduleCreate(BaseSchema):
    vehicle_id: int
    service_type: str
    scheduled_date: date
    odometer_threshold: Optional[float] = None
    notes: Optional[str] = None


class ServiceScheduleUpdate(BaseSchema):
    vehicle_id: Optional[int] = None
    service_type: Optional[str] = None
    scheduled_date: Optional[date] = None
    odometer_threshold: Optional[float] = None
    status: Optional[ServiceStatus] = None
    notes: Optional[str] = None


# ── ServiceHistory ────────────────────────────────────────────────────────────

class ServiceHistoryBase(BaseSchema):
    vehicle_id: int
    service_schedule_id: Optional[int] = None
    description: str
    cost: float
    service_date: date
    workshop: str
    odometer_service: float


class ServiceHistoryCreate(ServiceHistoryBase):
    pass


class ServiceHistoryUpdate(BaseSchema):
    vehicle_id: Optional[int] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    service_date: Optional[date] = None
    workshop: Optional[str] = None
    odometer_service: Optional[float] = None


class ServiceHistoryOut(ServiceHistoryBase):
    id: int


class ServiceScheduleOut(ServiceScheduleBase):
    id: int
    created_at: datetime
    history: List[ServiceHistoryOut] = []


# ── UsageLog ──────────────────────────────────────────────────────────────────

class UsageLogBase(BaseSchema):
    booking_id: int
    vehicle_id: int
    driver_id: int
    odometer_start: float
    odometer_end: Optional[float] = None
    departure: datetime
    return_datetime: Optional[datetime] = None


class UsageLogCreate(BaseSchema):
    booking_id: int
    vehicle_id: int
    driver_id: int
    odometer_start: float
    departure: datetime


class UsageLogUpdate(BaseSchema):
    odometer_end: Optional[float] = None
    return_datetime: Optional[datetime] = None
    odometer_start: Optional[float] = None
    departure: Optional[datetime] = None


class UsageLogOut(UsageLogBase):
    id: int
