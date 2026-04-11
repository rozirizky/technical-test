from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional, List
from app.models.vehicle import VehicleStatus, DriverStatus


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ── Vehicle ───────────────────────────────────────────────────

class VehicleBase(BaseSchema):
    plate_number: str
    brand: str
    model: str
    type: str
    year: int
    ownership_type: str
    location_id: Optional[int] = None
    status: VehicleStatus = VehicleStatus.available


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseSchema):
    plate_number: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    type: Optional[str] = None
    year: Optional[int] = None
    ownership_type: Optional[str] = None
    location_id: Optional[int] = None
    status: Optional[VehicleStatus] = None


class VehicleOut(VehicleBase):
    id: int
    created_at: datetime
    drivers: List["DriverOut"] = []


# ── Driver ────────────────────────────────────────────────────

class DriverBase(BaseSchema):
    user_id: int
    vehicle_id: Optional[int] = None
    license_number: str
    license_type: str
    license_expiry: date
    status: DriverStatus = DriverStatus.active


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseSchema):
    vehicle_id: Optional[int] = None
    license_number: Optional[str] = None
    license_type: Optional[str] = None
    license_expiry: Optional[date] = None
    status: Optional[DriverStatus] = None


class DriverOut(DriverBase):
    id: int
