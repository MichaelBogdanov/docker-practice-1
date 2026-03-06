# Задача 06 — Местные заметки о погоде

## Участники группы
Евкачев Р. Р.
Копаева Е. С.

## Описание: 
Короткие пользовательские заметки о погоде в городе.

## Endpoints:
POST /reports - { "city":"ttp://localhost:5000/reports?city=moscow","text":"sunny","temp":12 }
GET /reports - список (?city=Великий%20Новгород)
GET /reports/recent - последние N записей

## Тело запроса:
json
{
    "city": "moscow",
    "text": "sunny",
    "temp": 12
}

## Тестовые curl-команды:
curl http://localhost:5000/reports
curl http://localhost:5000/reports?city=moscow
curl -X POST http://localhost:5000/reports -H "Content-Type: application/json" -d '{"city":"moscow","text":"sunny","temp":12}'
curl http://localhost:5000/reports/recent

## Как запустить
docker compose up --build
API будет доступно по адресу: http://localhost:5000

## Примеры использования

# Создание заметки
curl -X POST http://localhost:5000/reports -H "Content-Type: application/json" -d '{"city":"moscow","text":"sunny","temp":12}'

# Получение всех заметок
curl http://localhost:5000/reports

# Получение заметок для конкретного города
curl http://localhost:5000/reports?city=moscow

# Получение последних заметок
curl http://localhost:5000/reports/recent