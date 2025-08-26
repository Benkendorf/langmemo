FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

CMD python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn --bind 0.0.0.0:8000 django_mem_cards.wsgi
