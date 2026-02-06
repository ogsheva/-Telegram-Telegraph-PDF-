#!/usr/bin/env python3
"""
Telegram Bot для конвертации статей Telegraph в PDF
Автор: Senior Python Developer
Версия: 1.0.0
"""

import os
import re
import logging
from pathlib import Path
from typing import Optional
import asyncio

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Константы
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TEMP_DIR = Path('./temp_pdfs')
TEMP_DIR.mkdir(exist_ok=True)

# Валидные домены
VALID_DOMAINS = ['telegra.ph', 'teletype.in', 'graph.org']

# CSS стили для PDF
PDF_STYLES = """
@page {
    margin: 2cm;
    size: A4;
}

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #333;
    max-width: 100%;
}

h1 {
    font-size: 24pt;
    font-weight: bold;
    margin-bottom: 0.5em;
    color: #000;
    text-align: center;
}

.author {
    text-align: center;
    font-style: italic;
    color: #666;
    margin-bottom: 2em;
    font-size: 11pt;
}

p {
    margin-bottom: 1em;
    text-align: justify;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1.5em auto;
    border-radius: 4px;
}

figure {
    margin: 1.5em 0;
    text-align: center;
}

figcaption {
    font-size: 10pt;
    color: #666;
    font-style: italic;
    margin-top: 0.5em;
}

blockquote {
    border-left: 4px solid #ddd;
    padding-left: 1em;
    margin: 1em 0;
    font-style: italic;
    color: #555;
}

code {
    background-color: #f5f5f5;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 10pt;
}

pre {
    background-color: #f5f5f5;
    padding: 1em;
    border-radius: 4px;
    overflow-x: auto;
}

a {
    color: #0066cc;
    text-decoration: none;
}

ul, ol {
    margin: 1em 0;
    padding-left: 2em;
}

li {
    margin-bottom: 0.5em;
}
"""


def validate_url(url: str) -> bool:
    """
    Проверяет, является ли URL корректным Telegraph/Teletype адресом
    
    Args:
        url: URL для проверки
        
    Returns:
        True если URL валиден, False в противном случае
    """
    pattern = r'^https?://(?:www\.)?(' + '|'.join(re.escape(domain) for domain in VALID_DOMAINS) + r')/.+'
    return bool(re.match(pattern, url))


def fetch_article(url: str) -> Optional[dict]:
    """
    Загружает и парсит статью с Telegraph
    
    Args:
        url: URL статьи
        
    Returns:
        Словарь с title, author, content (HTML) или None при ошибке
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Извлекаем заголовок
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else 'Без названия'
        
        # Извлекаем автора
        author_tag = soup.find('a', {'rel': 'author'}) or soup.find('address')
        author = author_tag.get_text(strip=True) if author_tag else 'Неизвестный автор'
        
        # Извлекаем основной контент
        article_tag = soup.find('article') or soup.find('div', class_='tl_article_content')
        
        if not article_tag:
            logger.error("Не удалось найти контент статьи")
            return None
        
        # Обрабатываем изображения: конвертируем относительные URL в абсолютные
        for img in article_tag.find_all('img'):
            if img.get('src'):
                img_src = img['src']
                if img_src.startswith('/'):
                    # Определяем базовый домен из URL
                    base_domain = re.match(r'(https?://[^/]+)', url).group(1)
                    img['src'] = base_domain + img_src
        
        # Получаем HTML контента
        content_html = str(article_tag)
        
        return {
            'title': title,
            'author': author,
            'content': content_html
        }
        
    except requests.RequestException as e:
        logger.error(f"Ошибка при загрузке статьи: {e}")
        return None
    except Exception as e:
        logger.error(f"Ошибка при парсинге статьи: {e}")
        return None


def generate_pdf(article_data: dict, output_path: Path) -> bool:
    """
    Генерирует PDF из данных статьи
    
    Args:
        article_data: Словарь с title, author, content
        output_path: Путь для сохранения PDF
        
    Returns:
        True если успешно, False при ошибке
    """
    try:
        # Создаем HTML документ
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>{article_data['title']}</title>
        </head>
        <body>
            <h1>{article_data['title']}</h1>
            <div class="author">Автор: {article_data['author']}</div>
            <div class="content">
                {article_data['content']}
            </div>
        </body>
        </html>
        """
        
        # Конфигурация шрифтов для WeasyPrint
        font_config = FontConfiguration()
        
        # Создаем CSS объект
        css = CSS(string=PDF_STYLES, font_config=font_config)
        
        # Генерируем PDF (совместимость с WeasyPrint 61.x и 62.x+)
        html = HTML(string=html_content)
        html.write_pdf(
            output_path,
            stylesheets=[css],
            font_config=font_config
        )
        
        logger.info(f"PDF успешно создан: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при генерации PDF: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_message = (
        "👋 Привет! Я бот для конвертации статей Telegraph в PDF.\n\n"
        "📝 Просто отправь мне ссылку на статью с:\n"
        "• telegra.ph\n"
        "• teletype.in\n"
        "• graph.org\n\n"
        "И я конвертирую её в красивый PDF-файл!\n\n"
        "ℹ️ Команды:\n"
        "/start - Показать это сообщение\n"
        "/help - Справка"
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_message = (
        "📖 Как пользоваться ботом:\n\n"
        "1️⃣ Найди статью на Telegraph или Teletype\n"
        "2️⃣ Скопируй ссылку на статью\n"
        "3️⃣ Отправь мне эту ссылку\n"
        "4️⃣ Дождись конвертации (обычно 5-10 секунд)\n"
        "5️⃣ Получи PDF-файл!\n\n"
        "⚠️ Важно: Ссылка должна быть полной, начинаться с http:// или https://\n\n"
        "Пример: https://telegra.ph/My-Article-01-01"
    )
    await update.message.reply_text(help_message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений с URL"""
    message_text = update.message.text.strip()
    
    # Проверяем валидность URL
    if not validate_url(message_text):
        await update.message.reply_text(
            "❌ Неверная ссылка!\n\n"
            "Пожалуйста, отправь корректную ссылку на статью с:\n"
            "• telegra.ph\n"
            "• teletype.in\n"
            "• graph.org\n\n"
            "Пример: https://telegra.ph/Example-Article-12-31"
        )
        return
    
    # Отправляем статус обработки
    status_message = await update.message.reply_text("⏳ Загружаю статью...")
    
    try:
        # Загружаем статью
        article_data = fetch_article(message_text)
        
        if not article_data:
            await status_message.edit_text(
                "❌ Не удалось загрузить статью.\n"
                "Проверьте, что ссылка корректна и статья существует."
            )
            return
        
        await status_message.edit_text("📄 Генерирую PDF...")
        
        # Генерируем уникальное имя файла
        safe_title = re.sub(r'[^\w\s-]', '', article_data['title'])[:50]
        pdf_filename = f"{safe_title}_{update.message.message_id}.pdf"
        pdf_path = TEMP_DIR / pdf_filename
        
        # Создаем PDF
        if not generate_pdf(article_data, pdf_path):
            await status_message.edit_text(
                "❌ Ошибка при создании PDF.\n"
                "Попробуйте позже или свяжитесь с администратором."
            )
            return
        
        await status_message.edit_text("📤 Отправляю файл...")
        
        # Отправляем PDF пользователю
        caption = f"📄 Вот ваша статья в PDF: {article_data['title']}"
        
        with open(pdf_path, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename=f"{safe_title}.pdf",
                caption=caption
            )
        
        # Удаляем сообщение о статусе
        await status_message.delete()
        
        # Удаляем временный файл
        pdf_path.unlink(missing_ok=True)
        logger.info(f"Успешно обработан запрос от пользователя {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        await status_message.edit_text(
            "❌ Произошла непредвиденная ошибка.\n"
            "Попробуйте позже."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Произошла ошибка при обработке вашего запроса.\n"
            "Попробуйте позже или обратитесь к администратору."
        )


def main() -> None:
    """Главная функция для запуска бота"""
    # Проверяем наличие токена
    if TELEGRAM_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error(
            "ОШИБКА: Токен не установлен!\n"
            "Установите переменную окружения TELEGRAM_BOT_TOKEN "
            "или замените YOUR_BOT_TOKEN_HERE в коде на ваш токен."
        )
        return
    
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Регистрируем обработчик текстовых сообщений (только URL)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    ))
    
    # Регистрируем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    logger.info("Бот запущен и готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
