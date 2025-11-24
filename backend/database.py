from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"
DATABASE_FILE = INSTANCE_DIR / "sales.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

INSTANCE_DIR.mkdir(exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


def get_session():
    return SessionLocal()


def init_database():
    from backend import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
