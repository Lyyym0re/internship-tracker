import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
import psycopg_pool
from app.api.applications import router as applications_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with psycopg_pool.AsyncConnectionPool(
        os.environ["DATABASE_URL"],
        open=False,
        min_size=1,
        max_size=2
    ) as pool:
        app.state.db_pool = pool
        yield

app = FastAPI(lifespan=lifespan)
app.include_router(applications_router)