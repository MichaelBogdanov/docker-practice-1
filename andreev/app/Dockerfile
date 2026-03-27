# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt внутрь контейнера
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# Копируем весь код приложения
COPY app8.py .

# Открываем порт 5000
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app8.py"]