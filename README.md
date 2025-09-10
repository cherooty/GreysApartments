## Greys Apart Bot — Telegram‑бот для аренды апартаментов в Санкт-Петербурге

Телеграм‑бот на базе aiogram 3, помогающий гостям Санкт‑Петербурга узнать об апартаментах, посмотреть описание/условия, а также получить подсказки по мероприятиям в городе. Хранение данных — PostgreSQL (asyncpg + SQLAlchemy 2.0 async).

Основные директории и файлы:
- `bot/main.py`, `bot/handlers.py`, `bot/about_apartments.py`, `bot/guide_spb.py` — логика бота и хендлеры
- `db.py`, `models.py`, `crud.py` — база данных, ORM‑модели и операции
- `startbot.sh` — скрипт запуска
- `requirements.txt` — зависимости

### Требования
- Python 3.10+
- PostgreSQL 13+

### Установка
1. Клонируйте репозиторий и перейдите в каталог проекта.
2. Создайте виртуальное окружение и активируйте его:
```bash
python3.10 -m venv venv1
source venv1/bin/activate
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```

### Настройка окружения
Создайте файл `.env` в корне проекта (рядом с `requirements.txt`) по примеру ниже или скопируйте из `.env.sample`:
```env
BOT_TOKEN=123456:ABCDEF_your_telegram_bot_token
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/greys_apart
```

Пояснения:
- `BOT_TOKEN` — токен Telegram‑бота от BotFather
- `DATABASE_URL` — строка подключения SQLAlchemy (драйвер `asyncpg` обязателен)

### Миграции/инициализация БД
При первом запуске приложение создаст таблицы автоматически на основе моделей (`db.init_db()`), отдельные миграции не требуются.

### Запуск
Вариант 1 — напрямую из Python:
```bash
python -m bot.main
```

Вариант 2 — через скрипт (создаёт venv, ставит зависимости, запускает):
```bash
chmod +x startbot.sh
./startbot.sh
```

### Полезные команды
- Проверка, что токен и БД‑URL подхватились: убедитесь, что `.env` лежит в корне и переменные `BOT_TOKEN` и `DATABASE_URL` заданы корректно. При отсутствии `DATABASE_URL` приложение завершится с ошибкой.

### Структура БД (кратко)
- `users` — Telegram‑пользователи
- `dialogs` — профиль/статистика диалогов
- `apartments`, `availability`, `bookings` — данные по объектам и бронированиям

### Лицензия
Проект распространяется по лицензии MIT. См. раздел ниже и файл `LICENSE` (если добавите отдельный файл).

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


