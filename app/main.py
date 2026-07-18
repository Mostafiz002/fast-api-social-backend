from fastapi import FastAPI
from app.routers import vote
from . import models
from .database import engine, database
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

database()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message" : "Hello World"}

