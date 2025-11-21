import uvicorn
from fastapi import FastAPI

from app.api.endpoints.currency import router as currency_router
from app.api.endpoints.users import router as user_router
from app.core.security import security

app = FastAPI()

app.include_router(user_router)
app.include_router(currency_router)
security.handle_errors(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=3)
