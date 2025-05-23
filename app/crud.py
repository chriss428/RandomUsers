import requests
from sqlalchemy import select, func, delete

from app.database import Session
from app.models import User
from app.schemas import User as UserSchema


def fetch_data(n: int):
    response = requests.get(f'https://randomuser.me/api/?results={n}')
    data_dict = response.json()["results"]

    with Session() as session:
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
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Database error: {e}")

def user_by_id(user_id: int) -> UserSchema:
    with Session() as session:
        query = select(User).where(User.id == user_id)
        result = session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return UserSchema.model_validate(user)
    return None

def random_user() -> UserSchema:
    with Session() as session:
        query = select(User).order_by(func.random())
        result = session.execute(query)
        user = result.scalars().first()
        if user:
            return UserSchema.model_validate(user)
    return None

def del_all_users():
    with Session() as session:
        data = delete(User)
        session.execute(data)
        session.commit()

def all_users(skip: int, limit: int):
    with Session() as session:
        query = select(User).offset(skip).limit(limit)
        result = session.execute(query)
        users = result.scalars().all()
        return [UserSchema.model_validate(user) for user in users]