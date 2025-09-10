from __future__ import annotations

"""Настройки подключения и сессии SQLAlchemy 2.0 (async)."""

import os
import logging

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ──────────────────────────────────────────────────────────────
# Загрузка переменных окружения
# ──────────────────────────────────────────────────────────────
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    logging.critical("❌ DATABASE_URL не задан в .env")
    raise RuntimeError("DATABASE_URL is required")

# ──────────────────────────────────────────────────────────────
# Базовый ORM-класс
# ──────────────────────────────────────────────────────────────
class Base(AsyncAttrs, DeclarativeBase):
    """Базовый ORM-класс. Все модели должны наследоваться от него."""


# ──────────────────────────────────────────────────────────────
# Движок и фабрика асинхронных сессий
# ──────────────────────────────────────────────────────────────
engine = create_async_engine(
    DB_URL,
    echo=False,          # можно временно включить True для отладки SQL
    pool_pre_ping=True,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Хелпер для dependency injection / FastAPI-style
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# ──────────────────────────────────────────────────────────────
# Инициализация БД — создание таблиц из моделей
# ──────────────────────────────────────────────────────────────
async def init_db() -> None:
    """Импортирует модели, регистрирует в metadata и создаёт таблицы."""
    import models  # ← критически важно! Без этого create_all не сработает

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
