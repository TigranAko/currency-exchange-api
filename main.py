from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from httpx import AsyncClient

from app.api.endpoints.currency import router as currency_router
from app.api.endpoints.users import router as user_router
from app.core.security import security
from app.dependencies.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    app.state.client = AsyncClient()
    yield
    await app.state.client.aclose()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(currency_router)
security.handle_errors(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=3)
