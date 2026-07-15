import time
from fastapi import Depends, FastAPI, Response
import psycopg
from psycopg.rows import dict_row 
from pydantic_settings import BaseSettings
from . import models
from .database import engine, database
from .routers import post, user, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

database()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message" : "Hello World"}


