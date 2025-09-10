#!/bin/bash

# 1. Создание виртуального окружения (если ещё не создано)
if [ ! -d "venv1" ]; then
    python3.10 -m venv venv1
fi

# 2. Активация виртуального окружения
source venv1/bin/activate

# 3. Установка зависимостей
pip install -r requirements.txt

# 4. Запуск бота
python -m bot.main
