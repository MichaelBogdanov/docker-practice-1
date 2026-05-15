#Используется Python 3.11 (инициализация или типа того :3)
FROM python:3.11-slim

#Рабочая папка
WORKDIR /app

#Зависимости из файла
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Копирует код приложения
COPY . .

#Открытие порта
EXPOSE 5000

#Запуск приложения
CMD ["python", "app.py"]