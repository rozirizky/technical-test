from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import Role
from loguru import logger


async def create(db: AsyncSession, data):
    try:
        role = Role(**data.model_dump())

        db.add(role)
        await db.commit()
        await db.refresh(role)

        logger.info(f"role created: {role.name}")

        return role

    except Exception as e:
        logger.exception(f"Error create role: {e}")
        await db.rollback()
        raise

async def get_all_role(db: AsyncSession):
    try:
        result = await db.execute(select(Role))
        roles = result.scalars().all()

        logger.info(f"Fetched {len(roles)} role")
        return roles

    except Exception as e:
        logger.exception(f"Error get all Roles: {e}")
        raise


async def get_Role_by_id(db: AsyncSession, Role_id: int):
    try:
      
        result = await db.execute(
            select(Role).where(Role.id == Role_id)
    )
        
        role = result.scalar_one_or_none()

        if not role:
            logger.warning(f"Role not found: {Role_id}")

        return role

    except Exception as e:
        logger.exception(f"Error get Role {Role_id}: {e}")
        raise


async def delete_Role(db: AsyncSession, Role_id: int):
    try:
        result = await db.execute(
            select(Role).where(Role.id == Role_id)
        )
        role = result.scalar_one_or_none()

        if not role:
            logger.warning(f"Delete failed, Role not found: {Role_id}")
            return False

        await db.delete(role)
        await db.commit()

        logger.info(f"Role deleted: {Role_id}")
        return True

    except Exception as e:
        logger.exception(f"Error delete Role {Role_id}: {e}")
        await db.rollback()
        raise


async def update_role(db: AsyncSession, role_id: int, data):
    try:
        stmt = select(Role).where(Role.id == role_id)
        result = await db.execute(stmt)
        role = result.scalar_one_or_none()

        if not role:
            logger.warning(f"Update failed, Role not found: {role_id}")
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(role, key, value)

        await db.commit()
        await db.refresh(role)

        logger.info(f"Role updated: {role_id}")
        return role

    except Exception as e:
        logger.exception(f"Error update Role {role_id}: {e}")
        await db.rollback()
        raise