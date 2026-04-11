from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.operational import FuelLog, ServiceSchedule, ServiceHistory, UsageLog
from loguru import logger


# ── FuelLog ───────────────────────────────────────────────────────────────────

async def create_fuel_log(db: AsyncSession, data):
    try:
        fuel_log = FuelLog(**data.model_dump())
        db.add(fuel_log)
        await db.commit()
        await db.refresh(fuel_log)

        logger.info(f"FuelLog created: vehicle_id={fuel_log.vehicle_id}, date={fuel_log.log_date}")
        return fuel_log

    except Exception as e:
        logger.exception(f"Error create fuel_log: {e}")
        await db.rollback()
        raise


async def get_all_fuel_logs(db: AsyncSession):
    try:
        result = await db.execute(select(FuelLog))
        logs = result.scalars().all()

        logger.info(f"Fetched {len(logs)} fuel_logs")
        return logs

    except Exception as e:
        logger.exception(f"Error get all fuel_logs: {e}")
        raise


async def get_fuel_log_by_id(db: AsyncSession, log_id: int):
    try:
        result = await db.execute(select(FuelLog).where(FuelLog.id == log_id))
        log = result.scalar_one_or_none()

        if not log:
            logger.warning(f"FuelLog not found: {log_id}")
        return log

    except Exception as e:
        logger.exception(f"Error get fuel_log {log_id}: {e}")
        raise


async def update_fuel_log(db: AsyncSession, log_id: int, data):
    try:
        result = await db.execute(select(FuelLog).where(FuelLog.id == log_id))
        log = result.scalar_one_or_none()

        if not log:
            logger.warning(f"Update failed, fuel_log not found: {log_id}")
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(log, key, value)

        await db.commit()
        await db.refresh(log)

        logger.info(f"FuelLog updated: {log_id}")
        return log

    except Exception as e:
        logger.exception(f"Error update fuel_log {log_id}: {e}")
        await db.rollback()
        raise


async def delete_fuel_log(db: AsyncSession, log_id: int):
    try:
        result = await db.execute(select(FuelLog).where(FuelLog.id == log_id))
        log = result.scalar_one_or_none()

        if not log:
            logger.warning(f"Delete failed, fuel_log not found: {log_id}")
            return False

        await db.delete(log)
        await db.commit()

        logger.info(f"FuelLog deleted: {log_id}")
        return True

    except Exception as e:
        logger.exception(f"Error delete fuel_log {log_id}: {e}")
        await db.rollback()
        raise


# ── ServiceSchedule ───────────────────────────────────────────────────────────

def _schedule_with_history():
    return select(ServiceSchedule).options(selectinload(ServiceSchedule.history))


async def create_service_schedule(db: AsyncSession, data):
    try:
        schedule = ServiceSchedule(**data.model_dump())
        db.add(schedule)
        await db.commit()
        await db.refresh(schedule)

        logger.info(f"ServiceSchedule created: vehicle_id={schedule.vehicle_id}, type={schedule.service_type}")

        result = await db.execute(
            _schedule_with_history().where(ServiceSchedule.id == schedule.id)
        )
        return result.scalar_one()

    except Exception as e:
        logger.exception(f"Error create service_schedule: {e}")
        await db.rollback()
        raise


async def get_all_service_schedules(db: AsyncSession):
    try:
        result = await db.execute(_schedule_with_history())
        schedules = result.scalars().all()

        logger.info(f"Fetched {len(schedules)} service_schedules")
        return schedules

    except Exception as e:
        logger.exception(f"Error get all service_schedules: {e}")
        raise


async def get_service_schedule_by_id(db: AsyncSession, schedule_id: int):
    try:
        result = await db.execute(
            _schedule_with_history().where(ServiceSchedule.id == schedule_id)
        )
        schedule = result.scalar_one_or_none()

        if not schedule:
            logger.warning(f"ServiceSchedule not found: {schedule_id}")
        return schedule

    except Exception as e:
        logger.exception(f"Error get service_schedule {schedule_id}: {e}")
        raise


async def update_service_schedule(db: AsyncSession, schedule_id: int, data):
    try:
        result = await db.execute(
            select(ServiceSchedule).where(ServiceSchedule.id == schedule_id)
        )
        schedule = result.scalar_one_or_none()

        if not schedule:
            logger.warning(f"Update failed, service_schedule not found: {schedule_id}")
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(schedule, key, value)

        await db.commit()
        await db.refresh(schedule)

        logger.info(f"ServiceSchedule updated: {schedule_id}")

        result = await db.execute(
            _schedule_with_history().where(ServiceSchedule.id == schedule.id)
        )
        return result.scalar_one()

    except Exception as e:
        logger.exception(f"Error update service_schedule {schedule_id}: {e}")
        await db.rollback()
        raise


async def delete_service_schedule(db: AsyncSession, schedule_id: int):
    try:
        result = await db.execute(
            select(ServiceSchedule).where(ServiceSchedule.id == schedule_id)
        )
        schedule = result.scalar_one_or_none()

        if not schedule:
            logger.warning(f"Delete failed, service_schedule not found: {schedule_id}")
            return False

        await db.delete(schedule)
        await db.commit()

        logger.info(f"ServiceSchedule deleted: {schedule_id}")
        return True

    except Exception as e:
        logger.exception(f"Error delete service_schedule {schedule_id}: {e}")
        await db.rollback()
        raise


# ── ServiceHistory ────────────────────────────────────────────────────────────

async def create_service_history(db: AsyncSession, data):
    try:
        history = ServiceHistory(**data.model_dump())
        db.add(history)
        await db.commit()
        await db.refresh(history)

        logger.info(f"ServiceHistory created: vehicle_id={history.vehicle_id}, date={history.service_date}")
        return history

    except Exception as e:
        logger.exception(f"Error create service_history: {e}")
        await db.rollback()
        raise


async def get_all_service_histories(db: AsyncSession):
    try:
        result = await db.execute(select(ServiceHistory))
        histories = result.scalars().all()

        logger.info(f"Fetched {len(histories)} service_histories")
        return histories

    except Exception as e:
        logger.exception(f"Error get all service_histories: {e}")
        raise


async def get_service_history_by_id(db: AsyncSession, history_id: int):
    try:
        result = await db.execute(
            select(ServiceHistory).where(ServiceHistory.id == history_id)
        )
        history = result.scalar_one_or_none()

        if not history:
            logger.warning(f"ServiceHistory not found: {history_id}")
        return history

    except Exception as e:
        logger.exception(f"Error get service_history {history_id}: {e}")
        raise


async def update_service_history(db: AsyncSession, history_id: int, data):
    try:
        result = await db.execute(
            select(ServiceHistory).where(ServiceHistory.id == history_id)
        )
        history = result.scalar_one_or_none()

        if not history:
            logger.warning(f"Update failed, service_history not found: {history_id}")
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(history, key, value)

        await db.commit()
        await db.refresh(history)

        logger.info(f"ServiceHistory updated: {history_id}")
        return history

    except Exception as e:
        logger.exception(f"Error update service_history {history_id}: {e}")
        await db.rollback()
        raise


async def delete_service_history(db: AsyncSession, history_id: int):
    try:
        result = await db.execute(
            select(ServiceHistory).where(ServiceHistory.id == history_id)
        )
        history = result.scalar_one_or_none()

        if not history:
            logger.warning(f"Delete failed, service_history not found: {history_id}")
            return False

        await db.delete(history)
        await db.commit()

        logger.info(f"ServiceHistory deleted: {history_id}")
        return True

    except Exception as e:
        logger.exception(f"Error delete service_history {history_id}: {e}")
        await db.rollback()
        raise


# ── UsageLog ──────────────────────────────────────────────────────────────────

async def create_usage_log(db: AsyncSession, data):
    try:
        usage_log = UsageLog(**data.model_dump())
        db.add(usage_log)
        await db.commit()
        await db.refresh(usage_log)

        logger.info(f"UsageLog created: booking_id={usage_log.booking_id}, vehicle_id={usage_log.vehicle_id}")
        return usage_log

    except Exception as e:
        logger.exception(f"Error create usage_log: {e}")
        await db.rollback()
        raise


async def get_all_usage_logs(db: AsyncSession):
    try:
        result = await db.execute(select(UsageLog))
        logs = result.scalars().all()

        logger.info(f"Fetched {len(logs)} usage_logs")
        return logs

    except Exception as e:
        logger.exception(f"Error get all usage_logs: {e}")
        raise


async def get_usage_log_by_id(db: AsyncSession, log_id: int):
    try:
        result = await db.execute(select(UsageLog).where(UsageLog.id == log_id))
        log = result.scalar_one_or_none()

        if not log:
            logger.warning(f"UsageLog not found: {log_id}")
        return log

    except Exception as e:
        logger.exception(f"Error get usage_log {log_id}: {e}")
        raise


async def update_usage_log(db: AsyncSession, log_id: int, data):
    try:
        result = await db.execute(select(UsageLog).where(UsageLog.id == log_id))
        log = result.scalar_one_or_none()

        if not log:
            logger.warning(f"Update failed, usage_log not found: {log_id}")
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(log, key, value)

        await db.commit()
        await db.refresh(log)

        logger.info(f"UsageLog updated: {log_id}")
        return log

    except Exception as e:
        logger.exception(f"Error update usage_log {log_id}: {e}")
        await db.rollback()
        raise


async def delete_usage_log(db: AsyncSession, log_id: int):
    try:
        result = await db.execute(select(UsageLog).where(UsageLog.id == log_id))
        log = result.scalar_one_or_none()

        if not log:
            logger.warning(f"Delete failed, usage_log not found: {log_id}")
            return False

        await db.delete(log)
        await db.commit()

        logger.info(f"UsageLog deleted: {log_id}")
        return True

    except Exception as e:
        logger.exception(f"Error delete usage_log {log_id}: {e}")
        await db.rollback()
        raise
