from time import time
from psycopg.rows import dict_row 
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic_settings import BaseSettings
from .config import settings
import psycopg

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"options": "-c search_path=public"} 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def database():
    while True:
        try:
            db_url = settings.DATABASE_URL
            if db_url.startswith("postgresql+psycopg://"):
                db_url = db_url.replace("postgresql+psycopg://", "postgresql://", 1)
            conn = psycopg.connect(conninfo=db_url, row_factory=dict_row)
            cursor = conn.cursor()
            print("[INFO] Database Connection is successful")
            break
        except Exception as error:
            print("[WARN] Database Connection failed")
            print("Error", error)
            time.sleep(2)