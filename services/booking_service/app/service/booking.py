from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.booking import Booking, Approval
from loguru import logger



def _booking_with_approvals():
    return select(Booking).options(selectinload(Booking.approvals))


async def create_booking(db: AsyncSession, data):
    try:
        booking = Booking(**data.model_dump())
        db.add(booking)
        await db.commit()
        await db.refresh(booking)

        logger.info(f"Booking created: {booking.booking_code}")

        result = await db.execute(
            _booking_with_approvals().where(Booking.id == booking.id)
        )
        return result.scalar_one()

    except Exception as e:
        logger.exception(f"Error create booking: {e}")
        await db.rollback()
        raise


async def get_all_bookings(db: AsyncSession):
    try:
        result = await db.execute(_booking_with_approvals())
        bookings = result.scalars().all()

        logger.info(f"Fetched {len(bookings)} bookings")
        return bookings

    except Exception as e:
        logger.exception(f"Error get all bookings: {e}")
        raise


async def get_booking_by_id(db: AsyncSession, booking_id: int):
    try:
        result = await db.execute(
            _booking_with_approvals().where(Booking.id == booking_id)
        )
        booking = result.scalar_one_or_none()

        if not booking:
            logger.warning(f"Booking not found: {booking_id}")

        return booking

    except Exception as e:
        logger.exception(f"Error get booking {booking_id}: {e}")
        raise


async def update_booking(db: AsyncSession, booking_id: int, data):
    try:
        result = await db.execute(
            select(Booking).where(Booking.id == booking_id)
        )
        booking = result.scalar_one_or_none()

        if not booking:
            logger.warning(f"Update failed, booking not found: {booking_id}")
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(booking, key, value)

        await db.commit()
        await db.refresh(booking)

        logger.info(f"Booking updated: {booking_id}")

        result = await db.execute(
            _booking_with_approvals().where(Booking.id == booking.id)
        )
        return result.scalar_one()

    except Exception as e:
        logger.exception(f"Error update booking {booking_id}: {e}")
        await db.rollback()
        raise


async def delete_booking(db: AsyncSession, booking_id: int):
    try:
        result = await db.execute(
            select(Booking).where(Booking.id == booking_id)
        )
        booking = result.scalar_one_or_none()

        if not booking:
            logger.warning(f"Delete failed, booking not found: {booking_id}")
            return False

        await db.delete(booking)
        await db.commit()

        logger.info(f"Booking deleted: {booking_id}")
        return True

    except Exception as e:
        logger.exception(f"Error delete booking {booking_id}: {e}")
        await db.rollback()
        raise



async def create_approval(db: AsyncSession, booking_id: int, data):
    try:
        approval = Approval(booking_id=booking_id, **data.model_dump())
        db.add(approval)
        await db.commit()
        await db.refresh(approval)

        logger.info(f"Approval created for booking {booking_id}, level {approval.level}")
        return approval

    except Exception as e:
        logger.exception(f"Error create approval: {e}")
        await db.rollback()
        raise


async def get_approvals_by_booking(db: AsyncSession, booking_id: int):
    try:
        result = await db.execute(
            select(Approval).where(Approval.booking_id == booking_id)
        )
        approvals = result.scalars().all()

        logger.info(f"Fetched {len(approvals)} approvals for booking {booking_id}")
        return approvals

    except Exception as e:
        logger.exception(f"Error get approvals for booking {booking_id}: {e}")
        raise


async def get_approval_by_id(db: AsyncSession, approval_id: int):
    try:
        result = await db.execute(
            select(Approval).where(Approval.id == approval_id)
        )
        approval = result.scalar_one_or_none()

        if not approval:
            logger.warning(f"Approval not found: {approval_id}")

        return approval

    except Exception as e:
        logger.exception(f"Error get approval {approval_id}: {e}")
        raise


async def update_approval(db: AsyncSession, approval_id: int, data):
    try:
        result = await db.execute(
            select(Approval).where(Approval.id == approval_id)
        )
        approval = result.scalar_one_or_none()

        if not approval:
            logger.warning(f"Update failed, approval not found: {approval_id}")
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(approval, key, value)

        await db.commit()
        await db.refresh(approval)

        logger.info(f"Approval updated: {approval_id}")
        return approval

    except Exception as e:
        logger.exception(f"Error update approval {approval_id}: {e}")
        await db.rollback()
        raise


async def delete_approval(db: AsyncSession, approval_id: int):
    try:
        result = await db.execute(
            select(Approval).where(Approval.id == approval_id)
        )
        approval = result.scalar_one_or_none()

        if not approval:
            logger.warning(f"Delete failed, approval not found: {approval_id}")
            return False

        await db.delete(approval)
        await db.commit()

        logger.info(f"Approval deleted: {approval_id}")
        return True

    except Exception as e:
        logger.exception(f"Error delete approval {approval_id}: {e}")
        await db.rollback()
        raise
