# Берём лёгкий образ Python
FROM python:3.11-slim

# Рабочая папка внутри контейнера
WORKDIR /app

# Сначала копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Создаём папку для базы данных
RUN mkdir -p /data

# Запускаем приложение
CMD ["python", "app.py"]
