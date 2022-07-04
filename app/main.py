from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import song, users, auth, vote
from .config import settings

print(settings.database_username)

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"Hello": "Pushing to Ubuntu"}


app.include_router(song.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
