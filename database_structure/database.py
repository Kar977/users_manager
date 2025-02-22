from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.environ.get("POSTGRES_USER") #"postgres"
PASSWORD = os.environ.get("POSTGRES_PASSWORD") #"password"
HOST = os.environ.get("POSTGRES_HOST") #"localhost"
PORT = os.environ.get("POSTGRES_PORT") #"5432"
DB_NAME = os.environ.get("POSTGRES_NAME") #"employee_manager_db"


#SYNC_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

def get_engine():#user: str, password: str, host: str, port: str, db: str):

    database_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}" #f"postgresql://{user}:{password}@{host}:{port}/{db}"

    if database_exists(database_url) == False:
        create_database(database_url)

    engine = create_engine(database_url, pool_size=50, echo=False)

    return engine


db_engine = get_engine() #"postgres", "password", "localhost", "5432", "user_manager_db")

SessionLocal = sessionmaker(bind=db_engine)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
