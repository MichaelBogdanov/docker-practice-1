from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import quotes, habits
from app.database import create_tables
from app.init_data import init_data
import logging

app = FastAPI(
    title="Практика 2: Docker наносит ответный удар",
    description="API(-шка)",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quotes.router, prefix="/quotes", tags=["Quotes"])
app.include_router(habits.router, prefix="/habits", tags=["Habits"])

logger = logging.getLogger("uvicorn.error")

@app.on_event("startup")
async def startup():
    await create_tables()
    await init_data()