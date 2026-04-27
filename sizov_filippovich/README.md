# Задание 8 — Метаданные картинок

## Участники
Сизов  
Филиппович

## Описание решения
HTTP API на Flask для хранения мета-информации об изображениях (url, width, height, tags).  
Данные хранятся в SQLite через Flask-SQLAlchemy. База данных живёт в Docker-томе и не теряется при перезапуске.

## Запуск
```bash
docker compose up --build
```

## Endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| POST | /images | Добавить изображение |
| GET | /images | Список всех (или фильтр по тегу `?tag=...`) |
| GET | /images/{id} | Детали одного изображения |

## Тестовые запросы

```bash
# Добавить изображение
curl -X POST http://localhost:5000/images \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/photo.jpg","width":800,"height":600,"tags":["landscape"]}'

# Получить все изображения
curl http://localhost:5000/images

# Фильтр по тегу
curl http://localhost:5000/images?tag=landscape

# Получить по id
curl http://localhost:5000/images/1
```
