from fastapi import FastAPI

from api.routers import post, user, auth, vote
from api.version import get_api_version

# Removing below command, since alembic is now handling DB creation+revisions
#models.Base.metadata.create_all(bind=engine)

version = get_api_version()

app = FastAPI(version=version)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():    
    return [{"message": "Hello World!"}, {"version": f"{version}"}]
