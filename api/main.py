import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from sqlalchemy.orm import Session
import psycopg
from psycopg.rows import dict_row

import crud, models, schemas, utils
from database import engine, get_db
from routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():    
    return {"message": "Hello World!"}