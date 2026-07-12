from typing import Optional
from random import randrange
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel 

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.get("/posts")
def get_posts(response: Response):
    if not my_posts:
        response.status_code = status.HTTP_404_NOT_FOUND
    return {"message" : my_posts}

@app.post("/posts", status_code=201)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    print(id)
    return {"post": post}