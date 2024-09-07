from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_db
from .routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # setup
    yield
    pass  # teardown


app = FastAPI(lifespan=lifespan)
app.include_router(router)
