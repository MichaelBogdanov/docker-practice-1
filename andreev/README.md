# Image Metadata API

REST API для хранения мета-информации об изображениях (URL, размеры, теги).

## Технологии

- Python 3.9+
- Flask
- Docker / Docker Compose

## Структура проекта
andreev/
├── app/
│ ├── app8.py # Основной код API
│ ├── Dockerfile # Инструкция для сборки Docker образа
│ └── requirements.txt # Зависимости Python
├── docker-compose.yml # Конфигурация Docker Compose
└── README.md

text

## Запуск

### Через Docker (рекомендуется)

```bash
cd andreev
docker-compose up --build
API будет доступно по адресу: http://localhost:5000

Локальный запуск
bash
cd andreev/app
pip install -r requirements.txt
python app8.py
API Endpoints
POST /images
Создание записи об изображении.

Тело запроса (JSON):

json
{
  "url": "https://example.com/image.jpg",
  "width": 800,
  "height": 600,
  "tags": ["landscape", "nature"]
}
Ответ: созданная запись с присвоенным ID
Статус: 201 Created

GET /images
Получение списка всех изображений.

Фильтрация по тегу:

text
GET /images?tag=landscape
Ответ: массив изображений

GET /images/{id}
Получение детальной информации об изображении.

Ответ: изображение с указанным ID
Статус 404: если изображение не найдено

Примеры запросов
Создание изображения
bash
curl -X POST http://localhost:5000/images \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/photo.jpg","width":800,"height":600,"tags":["landscape"]}'
Получение всех изображений
bash
curl http://localhost:5000/images
Фильтрация по тегу
bash
curl "http://localhost:5000/images?tag=portrait"
Получение изображения по ID
bash
curl http://localhost:5000/images/1