from fastapi import FastAPI

from routers import post, user, auth, vote
from version import get_version

# Removing below command, since alembic is now handling DB creation+revisions
#models.Base.metadata.create_all(bind=engine)

version = get_version()

app = FastAPI(version=version)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():    
    return [{"message": "Hello World!"}, {"version": f"{version}"}]
