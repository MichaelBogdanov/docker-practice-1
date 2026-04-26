# Описание реализованной задачи 

## Задача 1
Описание: хранилище коротких цитат с возможностью фильтрации по тегу и получения случайной цитаты.

Endpoints:

GET /quotes - список (опционально ?tag=life&limit=10)
GET /quotes/random - случайная цитата (?tag=...)
POST /quotes - добавить { "text": "...", "author": "...", "tags": ["..."] }
DELETE /quotes/{id} - удалить

## что сделано
Простое хранилище, где можно:
- Получить список цитат
- Получить случайную цитату, Можно фильтровать по тегу
- Добавить новую цитату
- Удалить цитату

## Какие есть команды?
1. Получить все цитаты
curl http://localhost:5000/quotes

2. Добавить новую цитату
curl -X POST http://localhost:5000/quotes 
-H "Content-Type: application/json" 
-d "{\"text\":\"www\",\"author\":\"Arsen\",\"tags\":[\"life\",\"motivation\"]}"


3. Получить цитаты отфильтрованные по тегу
curl "http://localhost:5000/quotes?tag=life"

4. Получить случайную цитату
curl http://localhost:5000/quotes/random

5. Удалить цитату
curl -X DELETE http://localhost:5000/quotes/1

Данные хранятся в памяти. При перезапуске контейнера все добавленные цитаты теряются

## Как запустить?
docker compose up --build