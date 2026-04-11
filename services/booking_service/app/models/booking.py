import enum
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base import Base


class BookingStatus(str, enum.Enum):
    draft     = "draft"
    pending   = "pending"
    approved  = "approved"
    rejected  = "rejected"
    ongoing   = "ongoing"
    done      = "done"
    cancelled = "cancelled"


class ApprovalStatus(str, enum.Enum):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected"


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    requester_id: Mapped[int] = mapped_column(Integer, nullable=False)
    vehicle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    driver_id: Mapped[int | None] = mapped_column(Integer)
    departure_datetime: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    return_datetime: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    passenger_count: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.draft)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    approvals: Mapped[list["Approval"]] = relationship("Approval", back_populates="booking")


class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), nullable=False)
    approver_id: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)  # 1, 2, 3...
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus), default=ApprovalStatus.pending)
    notes: Mapped[str | None] = mapped_column(Text)
    approved_at: Mapped[DateTime | None] = mapped_column(DateTime)

    booking: Mapped["Booking"] = relationship("Booking", back_populates="approvals")
