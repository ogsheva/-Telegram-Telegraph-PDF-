#!/bin/bash

# Скрипт запуска Telegraph PDF Bot
# Использование: bash start.sh

set -e

# Цвета
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "======================================"
echo "Telegraph PDF Bot - Start"
echo "======================================"
echo ""

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo -e "${RED}✗ Виртуальное окружение не найдено${NC}"
    echo -e "${YELLOW}→ Запустите сначала: bash deploy.sh${NC}"
    exit 1
fi

# Активация виртуального окружения
echo -e "${YELLOW}→ Активация виртуального окружения...${NC}"
source venv/bin/activate

# Проверка токена
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    if [ -f ".env" ]; then
        echo -e "${YELLOW}→ Загрузка токена из .env...${NC}"
        export $(grep -v '^#' .env | xargs)
    fi
    
    if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" = "your_bot_token_here" ]; then
        echo -e "${RED}✗ Токен бота не установлен${NC}"
        echo ""
        echo "Установите токен одним из способов:"
        echo "1. export TELEGRAM_BOT_TOKEN='ваш_токен'"
        echo "2. Отредактируйте файл .env"
        echo ""
        exit 1
    fi
fi

echo -e "${GREEN}✓ Токен найден${NC}"
echo -e "${GREEN}✓ Запуск бота...${NC}"
echo ""

# Запуск бота
python main.py
