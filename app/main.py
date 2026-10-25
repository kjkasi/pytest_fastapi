from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_db
from .routers.tasks import router as tasks_router


def create_app(*, initialize_database: bool = True) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        if initialize_database:
            init_db()
        yield

    application = FastAPI(
        title="FastAPI Repository Demo",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.include_router(tasks_router)
    return application


app = create_app()
