import time
from typing import Optional
from random import randrange
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
import psycopg
from psycopg.rows import dict_row 
from pydantic import BaseModel 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

my_posts = [
    {
        "id" : 1,
        "title" : "post 1",
        "content" : "hi this is me 1", 
    },
    {
        "id" : 2,
        "title" : "post 2",
        "content" : "hi this is me 2", 
    }
]

while True:
    try:
        conn = psycopg.connect(conninfo=settings.DATABASE_URL, row_factory=dict_row)
        cursor = conn.cursor()
        print("Database Connection is successful")
        break
    except Exception as error:
        print("Database Connection failed")
        print("Error", error)
        time.sleep(2)

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.get("/posts")
def get_posts(response: Response):
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts)
    return {"data" : posts}

@app.post("/posts", status_code=201)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id=%s", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return {"post": post}

@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return Response(status_code=204)