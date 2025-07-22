# О проекте LangMemo
LangMemo - это платформа для изучения иностранных языков с помощью метода Spaced Repetition System (SRS).
Внесенные пользователем слова предлагаются для повторения через промежутки времени, зависящие от успешности их изучения.

Слова представляются как карты, собираемые в колоды. Можно создавать несколько колод. Например для нескольких языков, или отдельные колоды для иероглифов и лексики.

## Ссылка на сайт
https://langmemo.ru

## API (WIP)
В разработке API для [Telegram бота-компаньона](https://github.com/Benkendorf/langmemo_bot), с помощью которого пользователь сможет проверять информацию о своем профиле в удобном формате мессенджера.

Аккаунт в Telegram привязывается к учетной записи LangMemo при помощи токена, генерируемого на сайте.

## Стек технологий

- Python 3.9
- Django 3.2.16
- Django REST Framework 3.12.4
- Djoser 2.1.0
- SimpleJWT 4.8.0
- PostgreSQL 13
- Docker, Docker Compose
- Gunicorn, Nginx
- Bootstrap

## Локальный запуск через Docker-compose

```bash
# 1. Клонируем репозиторий
git clone git@github.com:Benkendorf/langmemo.git

# 2. Создаем в корневой папке файл .env и заполняем по примеру
POSTGRES_USER=USERNAME
POSTGRES_PASSWORD=PASSWORD
POSTGRES_DB=DB_NAME

DB_HOST=db
DB_PORT=5432

SECRET_KEY=KEY_EXAMPLE
DEBUG=False
ALLOWED_HOSTS=127.0.0.1, localhost
USE_SQLITE=False

# 4. Поднимаем контейнеры
docker compose -f docker-compose.yml up --build
