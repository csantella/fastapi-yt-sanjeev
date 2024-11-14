from fastapi import FastAPI

import models
from config import settings
from database import engine
from routers import post, user, auth, vote


print(f"settings: {settings.model_dump()}")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():    
    return {"message": "Hello World!"}