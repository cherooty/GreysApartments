"""Маршрутизация и обработчики команд/кнопок (aiogram 3).

Экспортируется функция ``register_routers()`` — именно её вызывает
``main.py`` при старте.
"""

from __future__ import annotations

from aiogram import F, Router, types, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from db import async_session
from crud import get_or_create_user
from .guide_spb import router as guide_spb_router
from .about_apartments import router as about_apartments_router
from .about_apartments import main_menu_kb


__all__ = ["register_routers"]

router = Router(name="main")

# ──────────────────────────────────────────────────────────────
# Клавиатуры
# ──────────────────────────────────────────────────────────────

KB_START = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="▶️ Start")]],
    resize_keyboard=True,
)

KB_MAIN = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔑 Забронировать")],  # большая кнопка
        [KeyboardButton(text="📋 Об апартаментах"), KeyboardButton(text="🗓️ Доступность и цены")],
        [KeyboardButton(text="📍 Гид по СПб"), KeyboardButton(text="❓ FAQ и помощь")],
    ],
    resize_keyboard=True,
)


# ──────────────────────────────────────────────────────────────
# Хендлеры
# ──────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    #print("🔥 Хендлер /start сработал!")  # ← временно
    """/start — стартовое приветствие + кнопка 'Старт'."""
    await message.answer(
        text=(
            "✨ <b>Апартаменты в центре Санкт-Петербурга</b> ✨\n"
            "Уют, стиль и комфорт — всего в нескольких кликах 🛏️\n"
            "Забронируйте свой идеальный отдых уже сегодня!\n\n"
            "👇 Нажмите кнопку <b></b>, чтобы продолжить."
        ),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="▶️ Start")]],
            resize_keyboard=True,
            one_time_keyboard=True  # 🔹 Кнопка скроется после нажатия
        )
    )

@router.message(Command("menu"))
@router.message(F.text == "▶️ Start")
#async def show_main_menu(message: types.Message) -> None:
#    await message.answer("Выберите раздел:", reply_markup=KB_MAIN)
async def show_main_menu(message: types.Message) -> None:
    from .about_apartments import main_menu_kb
    await message.answer(
        "Выберите, пожалуйста, интересующий раздел в Главном меню 📋",
        reply_markup=KB_MAIN
    )

@router.message(F.text == "🔙 Назад")
async def back_to_main(message: types.Message) -> None:
    await message.answer("Вы в главном меню.", reply_markup=KB_MAIN)


# ──────────────────────────────────────────────────────────────
# Регистрация роутера в Dispatcher
# ──────────────────────────────────────────────────────────────

def register_routers(dp: Dispatcher) -> None:
    dp.include_router(router)
    dp.include_router(guide_spb_router)
    dp.include_router(about_apartments_router)


@router.message(F.text == "🔑 Забронировать")
async def booking_placeholder(message: types.Message):
    await message.answer(
        "🔧 Тут будет модуль бронирования!\nВы сможете выбрать даты, апартаменты и забронировать прямо в боте."
    )