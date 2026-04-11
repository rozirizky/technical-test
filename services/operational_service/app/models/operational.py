import enum
from sqlalchemy import Integer, String, Text, Float, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base import Base


class ServiceStatus(str, enum.Enum):
    scheduled = "scheduled"
    done      = "done"
    overdue   = "overdue"
    cancelled = "cancelled"


class FuelLog(Base):
    __tablename__ = "fuel_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    booking_id: Mapped[int | None] = mapped_column(Integer)
    liters: Mapped[float] = mapped_column(Float, nullable=False)
    odometer: Mapped[float] = mapped_column(Float, nullable=False)
    log_date: Mapped[Date] = mapped_column(Date, nullable=False)


class ServiceSchedule(Base):
    __tablename__ = "service_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    service_type: Mapped[str] = mapped_column(String(100), nullable=False)
    scheduled_date: Mapped[Date] = mapped_column(Date, nullable=False)
    odometer_threshold: Mapped[float | None] = mapped_column(Float)
    status: Mapped[ServiceStatus] = mapped_column(Enum(ServiceStatus), default=ServiceStatus.scheduled)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    history: Mapped[list["ServiceHistory"]] = relationship("ServiceHistory", back_populates="schedule")


class ServiceHistory(Base):
    __tablename__ = "service_histories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    service_schedule_id: Mapped[int | None] = mapped_column(ForeignKey("service_schedules.id"))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    service_date: Mapped[Date] = mapped_column(Date, nullable=False)
    workshop: Mapped[str] = mapped_column(String(150), nullable=False)
    odometer_service: Mapped[float] = mapped_column(Float, nullable=False)

    schedule: Mapped["ServiceSchedule | None"] = relationship("ServiceSchedule", back_populates="history")


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_id: Mapped[int] = mapped_column(Integer, nullable=False)
    vehicle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    driver_id: Mapped[int] = mapped_column(Integer, nullable=False)
    odometer_start: Mapped[float] = mapped_column(Float, nullable=False)
    odometer_end: Mapped[float | None] = mapped_column(Float)
    departure: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    return_datetime: Mapped[DateTime | None] = mapped_column(DateTime)
