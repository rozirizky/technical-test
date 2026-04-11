import enum
from sqlalchemy import Integer, String, ForeignKey, DateTime, Date, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class VehicleStatus(str, enum.Enum):
    available   = "available"
    in_use      = "in_use"
    maintenance = "maintenance"
    inactive    = "inactive"


class DriverStatus(str, enum.Enum):
    active   = "active"
    inactive = "inactive"
    on_leave = "on_leave"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plate_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    ownership_type: Mapped[str] = mapped_column(String(30), nullable=False)  # dinas/sewa
    location_id: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[VehicleStatus] = mapped_column(Enum(VehicleStatus), default=VehicleStatus.available)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    drivers: Mapped[list["Driver"]] = relationship(
        "Driver", back_populates="vehicle", foreign_keys="Driver.vehicle_id"
    )


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    vehicle_id: Mapped[int | None] = mapped_column(ForeignKey("vehicles.id"))
    license_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    license_type: Mapped[str] = mapped_column(String(10), nullable=False)  # A, B1, B2
    license_expiry: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[DriverStatus] = mapped_column(Enum(DriverStatus), default=DriverStatus.active)

    vehicle: Mapped["Vehicle | None"] = relationship(
        "Vehicle", back_populates="drivers", foreign_keys=[vehicle_id]
    )
