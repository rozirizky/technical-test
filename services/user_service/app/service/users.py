from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from loguru import logger
from sqlalchemy.orm import selectinload
from app.service.auth import hash_password

async def create(db: AsyncSession, data):
    try:
        user_data = data.model_dump()
        user_data['password'] = hash_password(user_data['password'])
        user = User(**user_data)

        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"User created: {user.email}")

        result = await db.execute(
            select(User).where(User.id == user.id).options(
                selectinload(User.role),
                selectinload(User.location)
            )
        )
        return result.scalar_one()

    except Exception as e:
        logger.exception(f"Error create user: {e}")
        await db.rollback()
        raise


async def get_all_users(db: AsyncSession):
    try:
        stmt = select(User).options(
        selectinload(User.role),
        selectinload(User.location)
    )
        result = await db.execute(stmt)
        users = result.scalars().all()

        logger.info(f"Fetched {len(users)} users")
        return users

    except Exception as e:
        logger.exception(f"Error get all users: {e}")
        raise

async def get_user_by_email(db: AsyncSession, email: str):
    try:
      
        result = await db.execute(
            select(User).where(User.email == email).options(
        selectinload(User.role),
        selectinload(User.location)
    )
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.warning(f"User not found: {email}")

        return user

    except Exception as e:
        logger.exception(f"Error get user {email}: {e}")
        raise

async def get_user_by_id(db: AsyncSession, user_id: int):
    try:
      
        result = await db.execute(
            select(User).where(User.id == user_id).options(
        selectinload(User.role),
        selectinload(User.location)
    )
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.warning(f"User not found: {user_id}")

        return user

    except Exception as e:
        logger.exception(f"Error get user {user_id}: {e}")
        raise


async def delete_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.warning(f"Delete failed, user not found: {user_id}")
            return False

        await db.delete(user)
        await db.commit()

        logger.info(f"User deleted: {user_id}")
        return True

    except Exception as e:
        logger.exception(f"Error delete user {user_id}: {e}")
        await db.rollback()
        raise


async def update_user(db: AsyncSession, user_id: int, data):
    try:
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            logger.warning(f"Update failed, user not found: {user_id}")
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)

        await db.commit()
        await db.refresh(user)
        logger.info(f"User updated: {user_id}")
        stmt = select(User).where(User.id == user.id).options(
            selectinload(User.role),
            selectinload(User.location)
        )

        result = await db.execute(stmt)
        return result.scalar_one()
        

    except Exception as e:
        logger.exception(f"Error update user {user_id}: {e}")
        await db.rollback()
        raise