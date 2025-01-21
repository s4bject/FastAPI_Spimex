FROM python:3.11-alpine3.16

WORKDIR /app

# Устанавливаем PostgreSQL клиент и libpq для версии 16.0
RUN apk update && \
    apk add --no-cache postgresql-client libpq

# Устанавливаем зависимости Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем приложение
COPY app /app

# Даем права на выполнение для init_db.sh и добавляем пользователя
RUN chmod +x /app/init_db.sh && \
    adduser --disabled-password --home /app s4bject && \
    chown -R s4bject:s4bject /app

USER s4bject

# Открываем порт для приложения
EXPOSE 8000

# Команда для запуска контейнера
CMD sh -c "sh /app/init_db.sh && uvicorn main:app --host 0.0.0.0 --port 8000"
