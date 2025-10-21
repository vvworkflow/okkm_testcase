from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.respondent import router as respondent_router
from src.core.db import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # закрываем пул при завершении
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(respondent_router)
