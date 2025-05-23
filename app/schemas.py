from pydantic import BaseModel


class UserBase(BaseModel):
    gender: str
    first_name: str
    last_name: str
    phone_number: str
    email: str
    country: str
    city: str
    street: str
    picture: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True