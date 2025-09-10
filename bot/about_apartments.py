from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp
from aiogram import types

#router = Router()
router = Router(name="about_apartments_spb")


# Память состояния (можно будет заменить на FSM или БД)
user_state = {}

# --------------------НАСТРОЙКА МЕНЮ-----------------------------------------------------------
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔑 Забронировать", callback_data="booking")],
        [InlineKeyboardButton(text="🏡 Об апартаментах", callback_data="about_apartments")],
        [InlineKeyboardButton(text="💵 Доступность и цены", callback_data="availability")],
        [InlineKeyboardButton(text="🗺️ Гид по СПб", callback_data="guide")],
        [InlineKeyboardButton(text="❓ FAQ и помощь", callback_data="faq")]
    ])

def apartments_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🌺 Апартаменты «Маки»", callback_data="apt_maki"),
            InlineKeyboardButton(text="🎷 Апартаменты «Блюз»", callback_data="apt_blues")
        ],
        [InlineKeyboardButton(text="📜 Правила проживания", callback_data="rules")],
        [InlineKeyboardButton(text="💰 Стоимость и условия", callback_data="pricing")]
    ])

def apartment_detail_kb(apartment):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📸 Фото апартаментов {apartment}", callback_data=f"photos_{apartment.lower()}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_apartments")],
        #[InlineKeyboardButton(text="📥 В главное меню", callback_data="to_main")]
    ])

def maki_detail_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📆 Посмотреть фото, выбрать даты и забронировать", callback_data="booking_maki")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_apartments")]
    ])

def blues_detail_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📆 Посмотреть фото, выбрать даты и забронировать", callback_data="booking_blues")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_apartments")]
    ])
#-----------------------------------------------------------------------------------------------------------------------

@router.message(F.text == "📋 Об апартаментах")

@router.callback_query(F.data == "about_apartments")
async def about_apartments(event):
    url = "https://docs.google.com/document/d/1jXjnvGqWk71aV-9NgOzPK5NUY5vCAVj8_JdRAbHrwqo/export?format=txt"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    doc_text = await response.text()
                else:
                    doc_text = "❌ Не удалось загрузить описание апарт-отеля."
    except Exception:
        doc_text = "⚠️ Ошибка при загрузке описания."

    if isinstance(event, types.Message):
        await event.answer(doc_text.strip())
        await event.answer("О чём рассказать подробнее?", reply_markup=apartments_kb())
    else:
        await event.message.answer(doc_text.strip())
        await event.message.answer("О чём рассказать подробнее?", reply_markup=apartments_kb())

# Действия при нажатии кнопки "Апартаменты "Маки"
@router.callback_query(F.data == "apt_maki")
async def show_maki(callback: CallbackQuery):
    # 1. Показываем титульное фото
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAPXaGWVrD9zSEYbp6iWlH8DBixMBuEAAijyMRtutChL8Vdqs_QmwkQBAAMCAAN5AAM2BA",
        caption="🌺 Апартаменты «Маки»"
    )
    
    # 2. Загружаем описание из Google Docs
    url = "https://docs.google.com/document/d/1PcNpUgMSdc9uVW77FhHJmeZTlOb9iXn9QIgoQvW_Zb8/export?format=txt"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                else:
                    text = "❌ Не удалось загрузить описание апартаментов «Маки»."
    except Exception:
        text = "⚠️ Ошибка при загрузке описания."

    # 3. Показываем описание + инлайн-кнопку на бронирование
    await callback.message.answer(text.strip(), reply_markup=maki_detail_kb())
    #await callback.message.edit_text(text.strip(), reply_markup=apartment_detail_kb("Маки"))

# Действия при нажатии кнопки "Апартаменты "Блюз"


@router.callback_query(F.data == "apt_blues")
async def show_blues(callback: CallbackQuery):
    # 1. Показываем титульное фото
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAPxaGWd7mNdPQHQvRqnZu2eI8oQC8cAAmb9MRvqIyhLCXgYK7Wxc_wBAAMCAAN5AAM2BA",
        caption="🎷 Апартаменты «Блюз»"
    )

    # 2. Загружаем описание из Google Docs
    url = "https://docs.google.com/document/d/14lmYVV3Vouoc7LWISzkLhUKNVlacau8UCWAKCbg-HPw/export?format=txt"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text() if response.status == 200 else "❌ Не удалось загрузить описание."
    except Exception:
        text = "⚠️ Ошибка при загрузке описания."

    # 3. Показываем описание с кнопкой бронирования
    await callback.message.answer(text.strip(), reply_markup=blues_detail_kb())



@router.callback_query(F.data.startswith("photos_"))
async def show_photos(callback: CallbackQuery):
    await callback.message.edit_text(
        "📸 Фото пока в разработке. Скоро вы сможете посмотреть фотогалерею.",
        reply_markup=apartments_kb()
    )

@router.callback_query(F.data == "back_main")
@router.callback_query(F.data == "to_main")
async def to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Вы в главном меню. Выберите раздел:",
        reply_markup=main_menu_kb()
    )

@router.callback_query(F.data == "back_apartments")
async def back_apartments(callback: CallbackQuery):
    await about_apartments(callback)

# Обработчик кнопки "Посмотреть фото, выбрать даты и забронировать" для "Маки"
@router.callback_query(F.data == "booking_maki")
async def show_booking_maki(callback: CallbackQuery):
    # Показываем сообщение со ссылкой
    await callback.message.edit_text(
        "📸 Актуальные фото и возможность бронирования наших апартаментов:\n\n"
        "👉 <a href='https://homereserve.ru/AABlHg'>Смотреть фото и забронировать</a>\n\n"
        "Вы перейдёте на нашу страницу с фото, ценами и кнопкой «Забронировать».",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_apartments")]
        ]),
        disable_web_page_preview=False
    )

@router.callback_query(F.data == "booking_blues")
async def show_booking_blues(callback: CallbackQuery):
    await callback.message.edit_text(
        "📸 Актуальные фото и возможность бронирования наших апартаментов:\n\n"
        "👉 <a href='https://homereserve.ru/AABlHg'>Смотреть фото и забронировать</a>\n\n"
        "Вы перейдёте на нашу страницу с фото, ценами и кнопкой «Забронировать».",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_apartments")]
        ]),
        disable_web_page_preview=False
    )


# 🔧 REPLY-еню: Обработчик кнопки "Забронировать"
# Сейчас выводит заглушку, в будущем заменим на полноценный сценарий выбора и бронирования
@router.callback_query(F.data == "booking")
async def show_booking_placeholder(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔧 Тут будет модуль бронирования!\nВы сможете выбрать даты, апартаменты и забронировать прямо в боте.",
        reply_markup=main_menu_kb()
    )


# 🔘 Обработчики inline-кнопок "Правила проживания" и "Стоимость и условия"
# Загружают текст из соответствующих Google Docs
@router.callback_query(F.data == "rules")
async def show_rules(callback: CallbackQuery):
    url = "https://docs.google.com/document/d/1owXB8gj_gXOMXfA_zg8KhUhzz3K24BroDGCSAMi9knc/export?format=txt"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text() if response.status == 200 else "❌ Не удалось загрузить правила проживания."
    except Exception:
        text = "⚠️ Ошибка при загрузке."

    await callback.message.edit_text(text.strip(), reply_markup=apartments_kb())

@router.callback_query(F.data == "pricing")
async def show_pricing(callback: CallbackQuery):
    url = "https://docs.google.com/document/d/1aIgmCAacPGXQGgtxAy6bQDBjVaH_nCuF5g3YuK9zmus/export?format=txt"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text() if response.status == 200 else "❌ Не удалось загрузить информацию о стоимости."
    except Exception:
        text = "⚠️ Ошибка при загрузке."

    await callback.message.edit_text(text.strip(), reply_markup=apartments_kb())

"""# ⬇️ Временный хендлер для получения file_id от Telegram
@router.message(F.photo)
async def catch_photo(message: Message):
    file_id = message.photo[-1].file_id
    print("📸 file_id:", file_id)
    await message.answer(f"✅ Фото получено! file_id:\n<code>{file_id}</code>")
"""
