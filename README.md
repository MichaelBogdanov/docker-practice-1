# TODO API в Docker

## Описание
Реализован простой HTTP API для управления задачами (TODO) с поддержкой:
- приоритета;
- срока выполнения;
- статуса задачи.

Используемые технологии:
- Python
- Flask
- SQLite
- Docker
- Docker Compose

## Структура проекта

```text
malyshev/
  app/
    app.py
    requirements.txt
    Dockerfile
  README.md
  docker-compose.yml