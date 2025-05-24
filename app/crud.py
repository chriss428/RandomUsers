import httpx
from sqlalchemy import select, func, delete
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.models import User
from app.schemas import User as UserSchema


async def fetch_data(n: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://randomuser.me/api/?results={n}')
        data_dict = response.json()["results"]


    async with async_session_maker() as session:
        try:
            for data in data_dict:
                user = User(
                    gender = data["gender"],
                    first_name = data["name"]["first"],
                    last_name = data["name"]["last"],
                    country = data["location"]["country"],
                    city = data["location"]["city"],
                    street = f'{data["location"]["street"]["number"]} {data["location"]["street"]["name"]}',
                    email = data["email"],
                    phone_number = data["phone"],
                    picture = data["picture"]["medium"]
                )

                session.add(user)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Database error: {e}")
            raise

async def user_by_id(user_id: int) -> UserSchema:
    async with async_session_maker() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return UserSchema.model_validate(user)
    return None

async def random_user() -> UserSchema:
    async with async_session_maker() as session:
        query = select(User).order_by(func.random())
        result = await session.execute(query)
        user = result.scalars().first()
        if user:
            return UserSchema.model_validate(user)
    return None

async def del_all_users():
    async with async_session_maker() as session:
        try:
            data = delete(User)
            await session.execute(data)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Database error: {e}")
            raise

async def all_users(skip: int, limit: int):
    async with async_session_maker() as session:
        try:
            query = select(User).offset(skip).limit(limit)
            result = await session.execute(query)
            users = result.scalars().all()
            return [UserSchema.model_validate(user) for user in users]
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            raise