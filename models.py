"""ORM‑модели SQLAlchemy 2.0 для Greys Apart Bot.

⚙️ Используем асинхронный движок (asyncpg) и декларативный стиль 2.0.
Базовый класс `Base` берётся из `db.py`.

Все связи настроены через `relationship`, а поля объявлены с помощью
`Mapped[]` и `mapped_column()` (типизировано для удобства IDE).
"""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

__all__ = [
    "User",
    "Dialog",
    "Apartment",
    "Event",
    "Availability",
    "Booking",
]


class User(Base):
    """Модель Telegram‑пользователя."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(128))
    last_name: Mapped[Optional[str]] = mapped_column(String(128))
    username: Mapped[Optional[str]] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()  # type: ignore[arg-type]
    )

    dialogs: Mapped[List["Dialog"]] = relationship(back_populates="user")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="user")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User tg_id={self.tg_id} username={self.username}>"


class Dialog(Base):
    """Профиль и статистика диалога пользователя."""

    __tablename__ = "dialogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(Text)
    last_name: Mapped[Optional[str]] = mapped_column(Text)
    username: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()  # type: ignore[arg-type]
    )
    last_interaction: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    total_sessions: Mapped[int] = mapped_column(Integer, default=0)
    total_messages: Mapped[int] = mapped_column(Integer, default=0)
    profile_summary: Mapped[str] = mapped_column(Text, default="")
    session_stats: Mapped[list] = mapped_column(JSONB, default=list)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="dialogs")


class Apartment(Base):
    """Каталог апартаментов."""

    __tablename__ = "apartments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[Optional[str]] = mapped_column(Text)
    capacity: Mapped[Optional[int]] = mapped_column(Integer)
    features: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))

    availability: Mapped[List["Availability"]] = relationship(back_populates="apartment")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="apartment")


class Event(Base):
    """Городские мероприятия (для агента‑гида)."""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    date: Mapped[date] = mapped_column(Date)
    location: Mapped[Optional[str]] = mapped_column(String(256))
    url: Mapped[Optional[str]] = mapped_column(String(512))


class Availability(Base):
    """Календарь доступности апартаментов."""

    __tablename__ = "availability"

    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"))
    date: Mapped[date] = mapped_column(Date)
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False)

    apartment: Mapped["Apartment"] = relationship(back_populates="availability")

    __table_args__ = (  # уникальный составной индекс на (apartment_id, date)
        {"sqlite_autoincrement": True},
    )


class Booking(Base):
    """Бронирования гостей."""

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"))
    from_date: Mapped[date] = mapped_column(Date)
    to_date: Mapped[date] = mapped_column(Date)
    price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()  # type: ignore[arg-type]
    )

    user: Mapped["User"] = relationship(back_populates="bookings")
    apartment: Mapped["Apartment"] = relationship(back_populates="bookings")

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<Booking user_id={self.user_id} apartment_id={self.apartment_id} "
            f"{self.from_date}->{self.to_date}>"
        )
