#!/bin/bash

# Скрипт автоматического развертывания Telegraph PDF Bot
# Использование: bash deploy.sh

set -e  # Остановка при ошибке

echo "======================================"
echo "Telegraph PDF Bot - Auto Deploy"
echo "======================================"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для цветного вывода
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Проверка ОС
print_info "Определение операционной системы..."
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    print_success "Обнаружен Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    print_success "Обнаружен macOS"
else
    print_error "Неподдерживаемая ОС: $OSTYPE"
    exit 1
fi

# Проверка Python
print_info "Проверка Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    print_success "Python установлен: версия $PYTHON_VERSION"
else
    print_error "Python 3 не найден. Установите Python 3.10 или выше"
    exit 1
fi

# Установка системных зависимостей
print_info "Установка системных зависимостей..."

if [ "$OS" = "linux" ]; then
    if command -v apt-get &> /dev/null; then
        print_info "Используется apt-get (Debian/Ubuntu)..."
        sudo apt-get update -qq
        sudo apt-get install -y -qq \
            python3-pip \
            python3-venv \
            libpango-1.0-0 \
            libpangoft2-1.0-0 \
            libgdk-pixbuf2.0-0 \
            libffi-dev \
            shared-mime-info
        print_success "Системные зависимости установлены"
    elif command -v dnf &> /dev/null; then
        print_info "Используется dnf (Fedora/RHEL)..."
        sudo dnf install -y \
            python3-pip \
            python3-virtualenv \
            pango \
            gdk-pixbuf2 \
            libffi-devel
        print_success "Системные зависимости установлены"
    else
        print_error "Неподдерживаемый менеджер пакетов"
        exit 1
    fi
elif [ "$OS" = "macos" ]; then
    if ! command -v brew &> /dev/null; then
        print_error "Homebrew не установлен. Установите с https://brew.sh"
        exit 1
    fi
    print_info "Используется Homebrew..."
    brew install python3 pango gdk-pixbuf libffi
    print_success "Системные зависимости установлены"
fi

# Создание виртуального окружения
print_info "Создание виртуального окружения..."
if [ -d "venv" ]; then
    print_info "Виртуальное окружение уже существует, пропускаем..."
else
    python3 -m venv venv
    print_success "Виртуальное окружение создано"
fi

# Активация виртуального окружения
print_info "Активация виртуального окружения..."
source venv/bin/activate
print_success "Виртуальное окружение активировано"

# Обновление pip
print_info "Обновление pip..."
pip install --upgrade pip -q
print_success "pip обновлен"

# Установка Python зависимостей
print_info "Установка Python пакетов..."
pip install -r requirements.txt -q
print_success "Python пакеты установлены"

# Создание директории для временных файлов
print_info "Создание директории для временных PDF..."
mkdir -p temp_pdfs
print_success "Директория создана"

# Проверка токена
echo ""
print_info "Настройка токена Telegram бота..."
if [ -f ".env" ]; then
    print_success "Файл .env найден"
else
    print_info "Файл .env не найден. Создаем из шаблона..."
    cp .env.example .env
    print_info "Отредактируйте файл .env и добавьте ваш токен бота"
    echo ""
    read -p "Введите токен бота (или нажмите Enter для ввода позже): " bot_token
    if [ -n "$bot_token" ]; then
        sed -i.bak "s/your_bot_token_here/$bot_token/" .env
        rm .env.bak 2>/dev/null || true
        print_success "Токен сохранен в .env"
    else
        print_info "Не забудьте добавить токен в .env перед запуском!"
    fi
fi

# Финальные инструкции
echo ""
echo "======================================"
print_success "Установка завершена!"
echo "======================================"
echo ""
echo "Следующие шаги:"
echo ""
echo "1. Убедитесь, что токен бота установлен:"
echo "   ${YELLOW}export TELEGRAM_BOT_TOKEN='ваш_токен'${NC}"
echo "   или отредактируйте файл .env"
echo ""
echo "2. Запустите бота:"
echo "   ${GREEN}source venv/bin/activate${NC}"
echo "   ${GREEN}python main.py${NC}"
echo ""
echo "Или используйте скрипт запуска:"
echo "   ${GREEN}bash start.sh${NC}"
echo ""
print_info "Справка и примеры: README.md, QUICKSTART.md, EXAMPLES.md"
echo ""
