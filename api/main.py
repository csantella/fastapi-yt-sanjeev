from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

import psycopg
from psycopg.rows import dict_row

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
    
conn = psycopg.connect('host=db port=5432 dbname=postgres user=postgres password=postgres',
                     row_factory=dict_row)

try:
    cursor = conn.cursor()
    

except BaseException:
    conn.rollback()
    
else:
    conn.commit()
    
finally:
    conn.close()


posts_db = [
    {"title": "How to make Pizza",
     "content": "The best pizza you've ever had",
     "id": 1
     }
    ]


def find_post(id: int):
    for p in posts_db:
        if p['id'] == id:
            return p
    
    return None


def get_index(id: int):
    for i, p in enumerate(posts_db):
        if p['id'] == id:
            return i
        
    return None


@app.get("/")
async def root():    
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"posts": posts_db }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post): # can be any variable name
    post_dict = post.model_dump()
    post_dict['id'] = randrange(1, 10000000)
    posts_db.append(post_dict)
    return { "message": "Post created." } | post_dict
    

@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{id} does not exist on the database.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id:{id} does not exist on the database."}
    else:
        return post
    
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = get_index(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Unable to delete post with id:{id}. Post was not found.")
        
    else:
        posts_db.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = get_index(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{id} was not found.")
    
    post_dict = post.model_dump()
    post_dict['id'] = int(id)
    posts_db[index] = post_dict
    
    return {"data": post_dict}
    