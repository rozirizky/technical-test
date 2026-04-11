from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.vehicle import Driver
from loguru import logger


async def create(db: AsyncSession, data):
    try:
        driver = Driver(**data.model_dump())

        db.add(driver)
        await db.commit()
        await db.refresh(driver)

        logger.info(f"Driver created: {driver.license_number}")
        return driver

    except Exception as e:
        logger.exception(f"Error create driver: {e}")
        await db.rollback()
        raise


async def get_all_drivers(db: AsyncSession):
    try:
        result = await db.execute(select(Driver))
        drivers = result.scalars().all()

        logger.info(f"Fetched {len(drivers)} drivers")
        return drivers

    except Exception as e:
        logger.exception(f"Error get all drivers: {e}")
        raise


async def get_driver_by_id(db: AsyncSession, driver_id: int):
    try:
        result = await db.execute(
            select(Driver).where(Driver.id == driver_id)
        )
        driver = result.scalar_one_or_none()

        if not driver:
            logger.warning(f"Driver not found: {driver_id}")

        return driver

    except Exception as e:
        logger.exception(f"Error get driver {driver_id}: {e}")
        raise


async def delete_driver(db: AsyncSession, driver_id: int):
    try:
        result = await db.execute(
            select(Driver).where(Driver.id == driver_id)
        )
        driver = result.scalar_one_or_none()

        if not driver:
            logger.warning(f"Delete failed, driver not found: {driver_id}")
            return False

        await db.delete(driver)
        await db.commit()

        logger.info(f"Driver deleted: {driver_id}")
        return True

    except Exception as e:
        logger.exception(f"Error delete driver {driver_id}: {e}")
        await db.rollback()
        raise


async def update_driver(db: AsyncSession, driver_id: int, data):
    try:
        stmt = select(Driver).where(Driver.id == driver_id)
        result = await db.execute(stmt)
        driver = result.scalar_one_or_none()

        if not driver:
            logger.warning(f"Update failed, driver not found: {driver_id}")
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(driver, key, value)

        await db.commit()
        await db.refresh(driver)

        logger.info(f"Driver updated: {driver_id}")
        return driver

    except Exception as e:
        logger.exception(f"Error update driver {driver_id}: {e}")
        await db.rollback()
        raise
