FROM python:3.11-alpine3.16

WORKDIR /app

# Устанавливаем необходимые пакеты
RUN apk add --no-cache postgresql-client libpq

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение и скрипт и даем права на выполнение
COPY app /app
RUN chmod +x /app/init_db.sh

# Создаем пользователя и меняем владельца папки
RUN adduser --disabled-password --home /app s4bject && \
    chown -R s4bject:s4bject /app

USER s4bject

# Открываем порт для приложения
EXPOSE 8000

# Устанавливаем команду по умолчанию
CMD ["/app/init_db.sh"]
