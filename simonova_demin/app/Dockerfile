FROM python:3.11-slim

# рабочая директория
WORKDIR /app

# копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ссоздание папки для бд
RUN mkdir -p /app/instance

#  порт
EXPOSE 5000

# запуск
CMD ["python", "app.py"]