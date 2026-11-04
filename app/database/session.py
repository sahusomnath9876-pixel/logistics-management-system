from .connection import db_engine
from sqlalchemy.orm import sessionmaker


db_engine = db_engine()

SessionLocal = sessionmaker(
    bind=db_engine,
    autoflush=False,
    autocommit=False
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

