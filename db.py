import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


def build_database_url() -> str:
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "relove")
    user = os.getenv("POSTGRES_USER", "relove")
    pwd = os.getenv("POSTGRES_PASSWORD", "relove")
    return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"


class Base(DeclarativeBase):
    pass


engine = create_engine(build_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


