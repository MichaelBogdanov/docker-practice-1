# Описание реализованной задачи 

## Задача 7
Описание: темы и сообщения в них (топики).

Endpoints:
POST /topics - { "title":"..." }
POST /topics/{id}/messages - { "author":"...","text":"..." }
GET /topics/{id}/messages - список сообщений

## что сделано
Простой форум, где можно:
- Создавать темы (например, "Фильмы", "Спорт", "Программирование")
- Писать сообщения в эти темы
- Читать что написали другие

## Какие есть команды?
1. Посмотреть все темы
curl http://localhost:5000/topics

2. Создать новую тему
curl -X POST http://localhost:5000/topics \
  -H "Content-Type: application/json" \
  -d '{"title":"Название темы"}'

3. Написать сообщение в тему
curl -X POST http://localhost:5000/topics/1/messages \
  -H "Content-Type: application/json" \
  -d '{"author":"Иван","text":"Привет!"}'

4. Прочитать сообщения из темы
curl http://localhost:5000/topics/1/messages

Хранит данные в SQLite
Данные хранятся в специальном Docker-томе message_data

## Как запустить?
docker-compose up --build