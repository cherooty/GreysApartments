"""Единственная helper‑функция для регистрации Telegram‑пользователя.

Пока боту достаточно только `get_or_create_user()`. Позже, когда появятся
новые сценарии (бронь, аналитика и т.д.), этот модуль расширится или
будет заменён на полноценный Repository‑Service слой.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User

__all__ = ["get_or_create_user"]

# ──────────────────────────────────────────────────────────
# Главная (и единственная) функция
# ──────────────────────────────────────────────────────────

async def get_or_create_user(
    session: AsyncSession,
    tg_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    username: str | None = None,
) -> User:
    """Возвращает пользователя, создавая запись при первом заходе.

    1. Ищем по `tg_id` (UNIQUE‑ключ).
    2. Если запись не найдена — создаём и коммитим.
    3. Всегда возвращаем актуальный объект `User`.
    """

    # 1️⃣ SELECT
    res = await session.execute(select(User).where(User.tg_id == tg_id))
    user: Optional[User] = res.scalar_one_or_none()

    # 2️⃣ INSERT (при необходимости)
    if user is None:
        user = User(
            tg_id=tg_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    # 3️⃣ Готово
    return user
