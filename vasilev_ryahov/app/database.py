import os
import logging
import asyncpg
from typing import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Database:
    "Класс для работы с базой данных"

    def __init__(self):
        """Инициализация конфига для подключения к БД"""

        self.pool: asyncpg.Pool | None = None
        self.CONFIG = {
            "host": os.getenv("DB_HOST", "db"),
            "port": int(os.getenv("DB_PORT", 5432)),
            "database": os.getenv("DB_NAME", "recipes_db"),
            "user": os.getenv("DB_USER", "user"),
            "password": os.getenv("DB_PASSWORD", "password"),
            "min_size": 1,
            "max_size": 10,
            "max_inactive_connection_lifetime": 300,
        }

    async def connect(self):
        """Создание пула, который подключается к БД"""
        self.pool = await asyncpg.create_pool(**self.CONFIG)
        logger.info("Подключение к database")

    async def disconnect(self):
        """Закрытие пула -> Отключение от БД"""
        if self.pool:
            await self.pool.close()
            logger.info("Отключение от database")

    async def get_connection(self) -> AsyncIterator[asyncpg.Connection]:
        """Получение соединение из пула"""
        if not self.pool:
            raise RuntimeError("Нет пула соединений к БД")

        async with self.pool.acquire() as conn:
            yield conn


db = Database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Механизм FastAPI для выполнения кода при запуске и при завершении приложения"""
    await db.connect()
    yield
    await db.disconnect()


async def get_db_connection(request: Request) -> AsyncIterator[asyncpg.Connection]:
    """FastAPI Depends() для получения соединения"""
    try:
        async for conn in db.get_connection():
            yield conn

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Ошибка подключения соединения: {e}")
        raise HTTPException(503, "База данных не доступна")
