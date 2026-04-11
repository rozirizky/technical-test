from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import Location
from loguru import logger


async def create(db: AsyncSession, data):
    try:
        location = Location(**data.model_dump())

        db.add(location)
        await db.commit()
        await db.refresh(location)

        logger.info(f"location created: {location.name}")

        return location

    except Exception as e:
        logger.exception(f"Error create location: {e}")
        await db.rollback()
        raise

async def get_all_locations(db: AsyncSession):
    try:
        result = await db.execute(select(Location))
        location = result.scalars().all()

        logger.info(f"Fetched {len(location)} location")
        return location

    except Exception as e:
        logger.exception(f"Error get all Locations: {e}")
        raise


async def get_location_by_id(db: AsyncSession, Location_id: int):
    try:
      
        result = await db.execute(
            select(Location).where(Location.id == Location_id)
    )
        
        location = result.scalar_one_or_none()

        if not location:
            logger.warning(f"Location not found: {Location_id}")

        return location

    except Exception as e:
        logger.exception(f"Error get Location {Location_id}: {e}")
        raise


async def delete_location(db: AsyncSession, Location_id: int):
    try:
        result = await db.execute(
            select(Location).where(Location.id == Location_id)
        )
        location = result.scalar_one_or_none()

        if not location:
            logger.warning(f"Delete failed, Location not found: {Location_id}")
            return False

        await db.delete(location)
        await db.commit()

        logger.info(f"Location deleted: {Location_id}")
        return True

    except Exception as e:
        logger.exception(f"Error delete Location {Location_id}: {e}")
        await db.rollback()
        raise


async def update_location(db: AsyncSession, location_id: int, data):
    try:
        stmt = select(Location).where(Location.id == location_id)
        result = await db.execute(stmt)
        location = result.scalar_one_or_none()

        if not location:
            logger.warning(f"Update failed, Location not found: {location_id}")
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(location, key, value)

        await db.commit()
        await db.refresh(location)

        logger.info(f"Location updated: {location_id}")
        return location

    except Exception as e:
        logger.exception(f"Error update Location {location_id}: {e}")
        await db.rollback()
        raise