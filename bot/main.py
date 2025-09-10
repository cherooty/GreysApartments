# bot/main.py
# E:
# cd E:\ProjectsLinux\arendaSPBot
# py -m venv .venv 
# .\.venv\Scripts\activate
# python -m pip install --upgrade pip
# pip install -r requirements.txt
# python -m bot.main

#Ubuntu: в корне
# python3.10 -m venv venv1
# source venv1/bin/activate
# ! pip install -r requirements.txt
# 


"""Точка входа для Greys Apart Bot (aiogram 3.20).

Запуск:
    (.venv) PS> python -m bot.main
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from .config import settings
from db import init_db
from .handlers import register_routers

BASE_DIR = Path(__file__).resolve().parent.parent  # корень проекта


def configure_logging() -> None:
    """Единая настройка логирования."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def create_bot() -> Bot:
    """Создаём экземпляр Bot (aiogram сам заведёт aiohttp‑сессию)."""
    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


async def main() -> None:
    configure_logging()

    # 1️⃣ Инициализируем БД (создаём таблицы при первом запуске)
    await init_db()

    # 2️⃣ Запускаем long‑polling
    bot = create_bot()
    dp = Dispatcher(storage=MemoryStorage())
    register_routers(dp)

    logging.info("🚀 Бот запущен…")
    await dp.start_polling(bot)


if __name__ == "__main__":  # pragma: no cover
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("⛔ Бот остановлен пользователем")
