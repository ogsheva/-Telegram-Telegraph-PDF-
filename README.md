<div align="center">

# 📄 Telegraph to PDF Bot

### 🤖 Telegram бот для конвертации статей Telegraph в красивые PDF файлы

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](Dockerfile)

[Возможности](#-возможности) • [Установка](#-установка) • [Использование](#-использование) • [Документация](#-документация) • [FAQ](#-faq)

![Demo](https://via.placeholder.com/800x400/0066cc/ffffff?text=Telegraph+%E2%86%92+PDF+Bot)

</div>

---

## 🌟 Возможности

<table>
<tr>
<td width="50%">

### 🚀 Для пользователей

- ✅ Конвертация **одной ссылкой**
- 🖼️ Сохранение **всех изображений**
- 🎨 **Профессиональное** оформление
- ⚡ Обработка за **5-10 секунд**
- 📱 Работает на **всех платформах**
- 🌍 Поддержка **кириллицы**

</td>
<td width="50%">

### 💻 Для разработчиков

- 🐍 Python 3.10+ с **async/await**
- 📦 **Production-ready** код
- 🐳 **Docker** & **docker-compose**
- 📚 **50+ страниц** документации
- 🛠️ Легко **кастомизируется**
- 🔧 **systemd** конфигурация

</td>
</tr>
</table>

---

## 🎯 Демонстрация

```
👤 Пользователь отправляет:
   https://telegra.ph/My-Great-Article-01-15

🤖 Бот отвечает:
   ⏳ Загружаю статью...
   📄 Генерирую PDF...
   📤 Отправляю файл...
   
   [📄 My Great Article.pdf]
   Вот ваша статья в PDF: My Great Article
```

<div align="center">

### 🎨 Результат

Профессионально оформленный PDF документ с:
- Красивыми шрифтами и отступами
- Всеми изображениями из статьи
- Информацией об авторе
- Сохранённым форматированием

</div>

---

## 📦 Быстрый старт

### 🪟 Windows

```powershell
# 1. Клонируйте репозиторий
git clone https://github.com/your-username/telegraph-pdf-bot.git
cd telegraph-pdf-bot

# 2. Создайте виртуальное окружение
python -m venv venv
venv\Scripts\activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Запустите бота
$env:TELEGRAM_BOT_TOKEN="ваш_токен_от_@BotFather"
python main.py
```

### 🐧 Linux / macOS

```bash
# Автоматическая установка
bash deploy.sh

# Запуск
export TELEGRAM_BOT_TOKEN="ваш_токен"
bash start.sh
```

### 🐳 Docker (рекомендуется)

```bash
docker-compose up -d
```

### 📱 Android (Termux)

Полная инструкция в [TERMUX_INSTALL.md](TERMUX_INSTALL.md)

---

## 🛠️ Технологический стек

```mermaid
graph LR
    A[Telegram Bot API] --> B[python-telegram-bot]
    C[Telegraph/Teletype] --> D[BeautifulSoup4]
    D --> E[HTML Parser]
    E --> F[WeasyPrint]
    F --> G[PDF Document]
    G --> A
```

### Основные библиотеки

| Библиотека | Версия | Назначение |
|-----------|--------|------------|
| **python-telegram-bot** | 21.0.1 | Асинхронный Telegram framework |
| **requests** | 2.31.0 | HTTP клиент |
| **beautifulsoup4** | 4.12.3 | Парсинг HTML |
| **weasyprint** | 61.2 | Генерация PDF |
| **pydyf** | 0.10.0 | PDF библиотека |
| **lxml** | 5.1.0 | XML/HTML парсер |
| **Pillow** | 10.2.0 | Обработка изображений |

---

## 📖 Документация

<table>
<tr>
<td width="50%">

### 🚀 Начало работы
- [README.md](README.md) — Полная инструкция
- [QUICKSTART.md](QUICKSTART.md) — Быстрый старт (5 мин)
- [EXAMPLES.md](EXAMPLES.md) — Примеры использования

### 🐛 Решение проблем
- [FAQ.md](FAQ.md) — Частые вопросы (50+ ответов)
- [WINDOWS_TROUBLESHOOTING.md](WINDOWS_TROUBLESHOOTING.md) — Проблемы Windows

</td>
<td width="50%">

### 📱 Специальные платформы
- [TERMUX_INSTALL.md](TERMUX_INSTALL.md) — Android (Termux)
- [TERMUX_CHEATSHEET.md](TERMUX_CHEATSHEET.md) — Шпаргалка команд

### 📋 Дополнительно
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — Структура проекта
- [CHANGELOG.md](CHANGELOG.md) — История изменений
- [config_example.py](config_example.py) — Расширенные настройки

</td>
</tr>
</table>

---

## ⚙️ Конфигурация

### Основные настройки

```python
# Переменные окружения
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather

# Или в config.py
VALID_DOMAINS = ['telegra.ph', 'teletype.in', 'graph.org']
TEMP_DIR = './temp_pdfs'
```

### Кастомизация PDF

```python
# Изменить стили в main.py
PDF_STYLES = """
body {
    font-family: 'Arial', sans-serif;
    font-size: 14pt;
    line-height: 1.8;
}

h1 {
    color: #0066cc;
    text-align: center;
}
"""
```

### Добавить watermark

```python
@page {
    @bottom-center {
        content: "Создано вашим ботом";
        font-size: 8pt;
        color: #999;
    }
}
```

---

## 🎨 Кастомизация

### Поддержка новых доменов

```python
VALID_DOMAINS = ['telegra.ph', 'teletype.in', 'graph.org', 'ваш-домен.com']
```

### Изменение шрифтов

```python
PDF_STYLES = """
body { font-family: 'Times New Roman', serif; }
"""
```

### Webhook режим

См. детали в [config_example.py](config_example.py)

---

## 🚀 Развертывание

### systemd (Linux)

```bash
sudo cp telegraph-bot.service /etc/systemd/system/
sudo systemctl enable telegraph-bot
sudo systemctl start telegraph-bot
```

### Docker

```bash
docker build -t telegraph-bot .
docker run -d --name telegraph-bot \
    -e TELEGRAM_BOT_TOKEN=your_token \
    --restart unless-stopped \
    telegraph-bot
```

### Heroku

```bash
heroku create your-app-name
git push heroku main
heroku config:set TELEGRAM_BOT_TOKEN=your_token
```

---

## 📊 Производительность

| Тип статьи | Время | Размер PDF |
|-----------|-------|-----------|
| 📝 Короткая (<1000 слов) | 2-5 сек | ~100 KB |
| 📄 Средняя (1000-3000 слов) | 5-10 сек | ~500 KB |
| 📚 Длинная (>3000 слов, 10+ фото) | 10-20 сек | 2-5 MB |

**Требования:**
- 💾 Минимум: 128 MB RAM, 200 MB диск
- ⚡ Рекомендуется: 512 MB RAM, 500 MB диск

---

## ❓ FAQ

<details>
<summary><b>Почему WeasyPrint, а не pdfkit?</b></summary>

| Критерий | pdfkit | WeasyPrint |
|----------|--------|-----------|
| Установка | Требует wkhtmltopdf | Чистый Python ✅ |
| Поддержка | Заброшен (2020) | Активная ✅ |
| Unicode | Проблемы | Отлично ✅ |
| Windows | Сложности | Работает ✅ |
| CSS3 | Ограниченная | Полная ✅ |

</details>

<details>
<summary><b>Бот не создаёт PDF (ошибка PDF.__init__)</b></summary>

```bash
pip uninstall pydyf -y
pip install pydyf==0.10.0
```

</details>

<details>
<summary><b>Как запустить в фоне на Linux?</b></summary>

```bash
# Вариант 1: screen
screen -S bot
python main.py
# Ctrl+A, затем D для отсоединения

# Вариант 2: systemd
sudo systemctl enable telegraph-bot
sudo systemctl start telegraph-bot
```

</details>

<details>
<summary><b>Можно ли запустить на Raspberry Pi?</b></summary>

Да! Следуйте инструкциям для Linux.

</details>

[Больше вопросов в FAQ.md](FAQ.md)

---

## 🤝 Вклад в проект

Вклады приветствуются! Вот как помочь:

1. 🍴 Форкните репозиторий
2. 🔧 Создайте ветку (`git checkout -b feature/amazing-feature`)
3. 💾 Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. 📤 Запушьте ветку (`git push origin feature/amazing-feature`)
5. 🎉 Создайте Pull Request

### TODO список

- [ ] Поддержка Medium, VC.ru, Habr
- [ ] Web интерфейс для управления
- [ ] Сохранение в Google Drive
- [ ] Форматы EPUB, MOBI
- [ ] Предпросмотр перед конвертацией
- [ ] OCR для изображений
- [ ] Мультиязычность

---

## 📜 Лицензия

Этот проект лицензирован под [MIT License](LICENSE).

```
MIT License

Copyright (c) 2025 Telegraph PDF Bot Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🌟 Авторы и благодарности

- **Разработчик:** [Your Name](https://github.com/your-username)
- **Документация:** Community Contributors
- **Тестирование:** Beta Testers

### Благодарности

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) — отличный фреймворк
- [WeasyPrint](https://weasyprint.org/) — мощная PDF библиотека
- [Telegraph](https://telegra.ph/) — за простой и красивый сервис

---

## 📞 Поддержка

Нужна помощь? Есть несколько вариантов:

- 📖 Прочитайте [документацию](README.md)
- ❓ Проверьте [FAQ](FAQ.md)
- 🐛 Создайте [Issue](https://github.com/your-username/telegraph-pdf-bot/issues)
- 💬 Присоединяйтесь к [обсуждениям](https://github.com/your-username/telegraph-pdf-bot/discussions)

---

## 📈 Статистика

![GitHub stars](https://img.shields.io/github/stars/your-username/telegraph-pdf-bot?style=social)
![GitHub forks](https://img.shields.io/github/forks/your-username/telegraph-pdf-bot?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/your-username/telegraph-pdf-bot?style=social)

![GitHub issues](https://img.shields.io/github/issues/your-username/telegraph-pdf-bot)
![GitHub pull requests](https://img.shields.io/github/issues-pr/your-username/telegraph-pdf-bot)
![GitHub last commit](https://img.shields.io/github/last-commit/your-username/telegraph-pdf-bot)

---

<div align="center">

### ⭐ Если проект помог — поставьте звезду!

**Сделано с ❤️ для сообщества**

[⬆ Вверх](#-telegraph-to-pdf-bot)

</div>
