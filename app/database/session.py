from .connection import db_engine
from sqlalchemy.orm import sessionmaker


db_engine = db_engine()

SessionLocal = sessionmaker(
    bind=db_engine,
    autoflush=False,
    autocommit=False
)


