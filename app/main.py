from pyexpat import model
import time
from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException
import psycopg
from psycopg.rows import dict_row 
from pydantic_settings import BaseSettings
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

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

# APIs
@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id=%s", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return post

@app.post("/posts", status_code=201, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 

    return new_post

@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=204)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post