# Задание 11 — Полив растений

HTTP API для отслеживания полива виртуальных растений.

## Реализация

- **Язык:** Python 3.11
- **Фреймворк:** Flask
- **База данных:** SQLite (файл хранится в Docker volume `/data/plants.db`)

## Запуск

```bash
docker compose up --build
```

API будет доступен по адресу `http://localhost:5000/`.

## Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/plants` | Список всех растений |
| `POST` | `/plants` | Добавить растение |
| `POST` | `/plants/{id}/water` | Отметить полив |
| `GET` | `/plants/{id}/status` | Статус растения |

## Примеры запросов

```bash
# Список растений
curl http://localhost:5000/plants

# Добавить растение
curl -X POST http://localhost:5000/plants \
  -H "Content-Type: application/json" \
  -d '{"name":"ficus","water_interval_days":7}'

# Отметить полив
curl -X POST http://localhost:5000/plants/1/water \
  -H "Content-Type: application/json" \
  -d '{"date":"2026-02-27"}'

# Получить статус
curl http://localhost:5000/plants/1/status
```

## Структура ответа `/plants/{id}/status`

```json
{
  "plant_id": 1,
  "name": "ficus",
  "water_interval_days": 7,
  "days_since_water": 3,
  "need_water": false
}
```

`need_water` становится `true`, если с момента последнего полива прошло столько же или больше дней, чем `water_interval_days`.
