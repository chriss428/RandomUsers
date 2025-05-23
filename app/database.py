from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import get_db_url

DATABASE_URL = get_db_url()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()