import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


def connection_url():
    load_dotenv()
    user= os.getenv("db_user")
    host= os.getenv("db_host")
    database= os.getenv("db_database")
    password= os.getenv("db_password")
    driver= os.getenv("driver_name")

    url = f"{driver}://{user}:{password}@{host}/{database}"
    return url


def engine():
    url = connection_url()

    if url:
        engine = create_engine(url)
        return engine
