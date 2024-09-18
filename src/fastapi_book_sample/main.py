from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_db
from .routers import router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()  # setup
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
