from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.vehicle import Vehicle
from loguru import logger


async def create(db: AsyncSession, data):
    try:
        vehicle = Vehicle(**data.model_dump())

        db.add(vehicle)
        await db.commit()
        await db.refresh(vehicle)

        logger.info(f"Vehicle created: {vehicle.plate_number}")

        result = await db.execute(
            select(Vehicle)
            .options(selectinload(Vehicle.drivers))
            .where(Vehicle.id == vehicle.id)
        )
        return result.scalar_one()

    except Exception as e:
        logger.exception(f"Error create vehicle: {e}")
        await db.rollback()
        raise


async def get_all_vehicles(db: AsyncSession):
    try:
        stmt = select(Vehicle).options(selectinload(Vehicle.drivers))
        result = await db.execute(stmt)
        vehicles = result.scalars().all()

        logger.info(f"Fetched {len(vehicles)} vehicles")
        return vehicles

    except Exception as e:
        logger.exception(f"Error get all vehicles: {e}")
        raise


async def get_vehicle_by_id(db: AsyncSession, vehicle_id: int):
    try:
        result = await db.execute(
            select(Vehicle)
            .options(selectinload(Vehicle.drivers))
            .where(Vehicle.id == vehicle_id)
        )
        vehicle = result.scalar_one_or_none()

        if not vehicle:
            logger.warning(f"Vehicle not found: {vehicle_id}")

        return vehicle

    except Exception as e:
        logger.exception(f"Error get vehicle {vehicle_id}: {e}")
        raise


async def delete_vehicle(db: AsyncSession, vehicle_id: int):
    try:
        result = await db.execute(
            select(Vehicle).where(Vehicle.id == vehicle_id)
        )
        vehicle = result.scalar_one_or_none()

        if not vehicle:
            logger.warning(f"Delete failed, vehicle not found: {vehicle_id}")
            return False

        await db.delete(vehicle)
        await db.commit()

        logger.info(f"Vehicle deleted: {vehicle_id}")
        return True

    except Exception as e:
        logger.exception(f"Error delete vehicle {vehicle_id}: {e}")
        await db.rollback()
        raise


async def update_vehicle(db: AsyncSession, vehicle_id: int, data):
    try:
        stmt = select(Vehicle).where(Vehicle.id == vehicle_id)
        result = await db.execute(stmt)
        vehicle = result.scalar_one_or_none()

        if not vehicle:
            logger.warning(f"Update failed, vehicle not found: {vehicle_id}")
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(vehicle, key, value)

        await db.commit()
        await db.refresh(vehicle)

        logger.info(f"Vehicle updated: {vehicle_id}")

        result = await db.execute(
            select(Vehicle)
            .options(selectinload(Vehicle.drivers))
            .where(Vehicle.id == vehicle.id)
        )
        return result.scalar_one()

    except Exception as e:
        logger.exception(f"Error update vehicle {vehicle_id}: {e}")
        await db.rollback()
        raise
