from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import post, user, auth, vote
from api._version import __version__ as version

# Removing below command, since alembic is now handling DB creation+revisions
#models.Base.metadata.create_all(bind=engine)

app = FastAPI(version=version)

origins = [
    "*", # refine later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():    
    return [{"message": "Hello World!"}, {"version": f"{version}"}]
