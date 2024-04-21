import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from sqlalchemy.orm import Session

import psycopg
from psycopg.rows import dict_row

import crud, models, schemas
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class MyDatabase(object):
    _retries: int = 3

    conn: psycopg.Connection = None
    cursor: psycopg.Cursor = None

    def __init__(self, dbname: str, host: str, port: int, user: str, password: str, retry: Optional[int]=3) -> None:
        self._retries = retry
        count = 0

        while count < self._retries:
            try:
                self.conn = psycopg.connect(f'host={host} port={port} dbname={dbname} user={user} password={password}',
                            row_factory=dict_row)
                
                self.cursor = self.conn.cursor()

                return

            except Exception as e:
                print(f"Exception occurred!\n{e}")
                count += 1
                print(f"Attempt {count}/{self._retries}", flush=True)
                time.sleep(3)

        raise ConnectionError
    
    def close_connection(self):
        if not self.conn.closed:
            del self.cursor
            self.conn.close()


db = MyDatabase(dbname="fastapi-yt-sanjeev", host="db", port=5432, user="postgres", password="postgres")


@app.get("/")
async def root():    
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """ INSERT INTO posts (title, content, published) 
            VALUES (%s, %s, %s) RETURNING *,
            (post.title, post.content, post.published))"""
    
    new_post = models.Post(**post.model_dump())
    
    # add new post object to the db
    db.add(new_post)

    # commit changes to db store
    db.commit()

    # replace 'new_post' with the refreshed version from the database
    db.refresh(new_post)

    return { "data": new_post }
    

@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    # """SELECT * FROM posts WHERE id = %s""", (id,))
    query_post = crud.get_post_by_id(db, id)

    if query_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")

    return { "post_detail": query_post }
    
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # """DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    del_post = crud.post_query_by_id(db, id)

    if del_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Unable to delete post with id:{id}. Post was not found.")
    
    del_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@app.put("/posts/{id}")
async def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    """
        UPDATE posts
        SET title = %s, content = %s, published = %s
        WHERE id = %s RETURNING *,
        (post.title, post.content, post.published, id))"""
    upd_query = crud.post_query_by_id(db, id)

    if upd_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{id} was not found.")
    
    upd_query.update(post.model_dump(),
                     synchronize_session=False)
    db.commit()
    return {"post_detail": upd_query.first()}
    