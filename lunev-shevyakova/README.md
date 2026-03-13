# Трекер привычек (Habit Tracker) - Вариант 4

**Студенты:** Лунёв Александр, Шевякова Алина

## Описание проекта
Простое HTTP API для отслеживания привычек. Позволяет создавать привычки, отмечать их выполнение по дням и подсчитывать текущую серию (streak).

## Запуск проекта
1.  Убедитесь, что Docker Desktop запущен.
2.  Откройте терминал в папке `lunev-shevyakova`.
3.  Выполните команду:
    ```bash
    docker-compose up --build
4. API станет доступно по адресу http://localhost:5000.

## Примеры запросов (curl)

1. Создать привычку:
curl -X POST http://localhost:5000/habits -H "Content-Type: application/json" -d "{\"name\":\"Пробежка\",\"user_id\":1}"

2. Отметить выполнение:
curl -X POST http://localhost:5000/habits/1/check -H "Content-Type: application/json" -d "{\"date\":\"2026-03-13\"}"

3. Получить streak:
curl http://localhost:5000/habits/1/streak

4. Посмотреть все привычки:
curl http://localhost:5000/habits