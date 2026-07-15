import time
from fastapi import Depends, FastAPI, Response
import psycopg
from psycopg.rows import dict_row 
from pydantic_settings import BaseSettings
from . import models
from .database import engine
from .routers import post, user

class Settings(BaseSettings):
    DATABASE_URL: str
    class Config:
        env_file = ".env"
settings = Settings()

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

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

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message" : "Hello World"}


