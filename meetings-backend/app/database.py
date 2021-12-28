from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

from app.config import settings

engine = create_engine(settings.database_url)


def get_session() -> Session:
    session = sessionmaker(engine, expire_on_commit=False)
    with session() as session:
        yield session
