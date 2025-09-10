# guide_spb.py

import asyncio
import datetime

import requests
from bs4 import BeautifulSoup
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

router = Router(name="guide_spb")


@router.message(F.text == "📍 Гид по СПб")
async def guide_select_start_date(message: types.Message, state: FSMContext):
    """
    Шаг 1: Пользователь нажал на «Гид по СПб» —
    показываем календарь для выбора даты начала.
    """
    # очищаем прежние данные, если они были
    await state.clear()
    await message.answer(
        "Выберите дату начала событий:",
        reply_markup=await SimpleCalendar(locale='ru_RU').start_calendar()
    )


@router.callback_query(SimpleCalendarCallback.filter())
async def process_calendar(
    callback_query: types.CallbackQuery,
    callback_data: dict,
    state: FSMContext
):
    """
    Обрабатываем клики по календарю.
    Сначала выбираем start_date, затем end_date.
    После выбора обоих дат — парсим Афишу и показываем события.
    """
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if not selected:
        # пользователь просто переключил месяц/год
        return

    data = await state.get_data()

    if "start_date" not in data:
        # Пользователь выбрал дату начала
        await state.update_data(start_date=date)
        await callback_query.message.answer(
            f"Начало: {date.strftime('%d.%m.%Y')}\nТеперь выберите дату окончания:",
            reply_markup=await SimpleCalendar(locale='ru_RU').start_calendar()
        )
    else:
        # Пользователь выбрал дату окончания
        start_date: datetime.date = data["start_date"]
        end_date: datetime.date = date
        await state.clear()
        await callback_query.message.answer(
            f"Выбраны даты: {start_date.strftime('%d.%m.%Y')} — {end_date.strftime('%d.%m.%Y')}",
            reply_markup=ReplyKeyboardRemove()
        )

        # Запускаем парсер в пуле потоков, чтобы не блокировать loop
        events = await asyncio.to_thread(parse_afisha, start_date, end_date)

        if not events:
            await callback_query.message.answer("Событий не найдено по указанным датам.")
            return

        # Выводим пользователю найденные события
        for ev in events:
            lines = [
                f"<b>{ev['title']}</b>",
                f"Категория: {ev['category']}",
                f"Дата / место: {ev['notice'] or '—'}",
                f"Цена: {ev['price']}",
                f"Рейтинг: {ev['rating']}",
            ]
            # Добавляем ссылку только если она непустая
            if ev.get("link"):
                lines.append(f"<a href=\"{ev['link']}\">Ссылка</a>")

            text = "\n".join(lines)
            await callback_query.message.answer(text, disable_web_page_preview=True)


def parse_afisha(start_date: datetime.date, end_date: datetime.date) -> list[dict]:
    """
    Синхронный парсер событий с afisha.ru по диапазону дат.
    Возвращает список словарей с полями:
    title, link, price, rating, category, notice.
    """
    # Форматируем даты в "d-m", убирая ведущие нули
    start = f"{start_date.day}-{start_date.month}"
    end   = f"{end_date.day}-{end_date.month}"
    year = start_date.year
    priority_param = f"prioritydates={year}-{start}--{year}-{end}"

    url = f"https://www.afisha.ru/spb/events/{start}_{end}/"
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/113.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=HEADERS, timeout=10)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all("div", {"data-test": "ITEM"})

    events: list[dict] = []
    for item in items:
        # Название
        title = item.get("aria-label") or (
            item.find("a", {"data-test": lambda x: x and "ITEM-NAME" in x})
            .get_text(strip=True)
        ) or "Без названия"

        # Ссылка
        a_tag = item.find("a", {"data-test": lambda x: x and "ITEM-URL" in x})
        link = a_tag["href"] if a_tag and a_tag.has_attr("href") else ""
        if link.startswith("/"):
            link = "https://www.afisha.ru" + link.rstrip("/")
        if link:
            link = link + (f"&{priority_param}" if "?" in link else f"/?{priority_param}")

        # ПРОПУСКАЕМ блоки без ссылки
        if not link:
            continue

        # Цена
        ticket_tag = item.find("a", {"data-test": lambda x: x and "TICKET-BUTTON" in x})
        price = ticket_tag.get_text(strip=True) if ticket_tag else "Нет цены"

        # Рейтинг
        rating_tag = item.find(attrs={"data-test": "RATING"})
        rating = rating_tag.get_text(strip=True) if rating_tag else "Нет рейтинга"

        # Категория
        category_tag = item.find(
            "div",
            {"data-test": lambda x: x and "ITEM-META" in x and "ITEM-NOTICE" not in x}
        )
        category = category_tag.get_text(strip=True) if category_tag else "Без категории"

        # Доп. информация
        notice_tag = item.find("div", {"data-test": lambda x: x and "ITEM-NOTICE" in x})
        notice = notice_tag.get_text(strip=True) if notice_tag else ""

        events.append({
            "title": title,
            "link": link,
            "price": price,
            "rating": rating,
            "category": category,
            "notice": notice
        })

    return events
