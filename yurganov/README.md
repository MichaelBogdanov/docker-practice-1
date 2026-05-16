# Трекер привычек

## Участники группы
Юрганов

## Описание решения
Простое HTTP API на Flask для отслеживания привычек. Данные хранятся в памяти. Реализованы эндпоинты для создания привычки, отметки выполнения и подсчета текущей серии (streak) подряд идущих дней.

## Как запустить
```bash
cd yurganov
docker compose up --build
```

## Тестовые запросы
```bash
curl http://localhost:5000/habits
curl -X POST http://localhost:5000/habits -H "Content-Type: application/json" -d '{"name":"Пробежка","user_id":1}'
curl -X POST http://localhost:5000/habits/1/check -H "Content-Type: application/json" -d '{"date":"2026-02-27"}'
curl http://localhost:5000/habits/1/streak
```
