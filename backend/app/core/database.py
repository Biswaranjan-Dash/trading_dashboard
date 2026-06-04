from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL, ADMIN_DATABASE_URL

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def ensure_database_exists():
    database_name = DATABASE_URL.rsplit("/", 1)[-1]
    admin_engine = create_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")

    with admin_engine.connect() as connection:
        exists = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :database_name"),
            {"database_name": database_name},
        ).scalar()

        if not exists:
            connection.execute(text(f'CREATE DATABASE "{database_name}"'))

def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()