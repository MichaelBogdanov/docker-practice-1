# Weather Reports API
### Выполнил: Иванов Кирилл 3991 (вариант 6)

Простое REST API приложение для создания и получения местных заметок о погоде. Позволяет пользователям оставлять короткие заметки о погоде в различных городах.


## Возможности

- Создание заметок о погоде с указанием города, текста и температуры
- Получение списка всех заметок
- Фильтрация заметок по городу
- Получение последних N заметок
- Хранение данных в SQLite базе данных
- Docker-контейнеризация для простого развертывания

## Технологии

- Python 3.12
- Flask (веб-фреймворк)
- SQLite (база данных)
- Docker / Docker Compose (контейнеризация)

## API Endpoints

| Метод | Endpoint | Описание | Параметры |
|-------|----------|----------|-----------|
| POST | `/reports` | Создание новой заметки, время погоды берётся текущее | JSON: `{"city": "moscow", "text": "sunny", "temp": 12}` |
| GET | `/reports` | Получение всех заметок | Для поиска по городу: `?city=moscow` (опционально, чувствительно к регистру) |
| GET | `/reports/recent` | Получение последних заметок | `?n=10` (опционально, по умолчанию 10, не более 100) |

## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/HanamileH/docker-practice-1
cd ivanov
cd app
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите приложение:
```bash
python app.py
```

4. Сервер запустится на `http://localhost:5000`

### Запуск через Docker

1. Убедитесь, что Docker и Docker Compose установлены

2. Соберите и запустите контейнер:
```bash
docker-compose up --build
```

3. Для запуска в фоновом режиме:
```bash
docker-compose up -d --build
```

4. Остановка контейнеров:
```bash
docker-compose down
```

## Примеры использования

### Создание заметки
```bash
curl -X POST http://localhost:5000/reports \
  -H "Content-Type: application/json" \
  -d '{"city":"moscow","text":"sunny","temp":12}'
```

### Получение всех заметок
```bash
curl http://localhost:5000/reports
```

### Фильтрация по городу
```bash
curl "http://localhost:5000/reports?city=moscow"
```

### Получение последних 5 заметок
```bash
curl "http://localhost:5000/reports/recent?n=5"
```