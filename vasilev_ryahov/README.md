# Recipe API

API для работы с рецептами. Хранит рецепты и ингредиенты, позволяет искать рецепты по наличию продуктов.

## Как запустить

1. Запустить Docker Desktop
2. Перейти в папку проекта:
```bash
cd vasilev_ryahov
```
3. Выполнить в терминале:
```bash
docker compose up --build
```

После запуска API доступен на http://localhost:5000

## Как остановить
```bash
docker compose down
```

## Endpoints 

- `GET /` — список всех endpoints
- `POST /recipes` — создать рецепт
- `GET /recipes` — все рецепты
- `GET /recipes?has=egg,milk` — рецепты с ингредиентами (можно указать match=all или match=any)
- `GET /recipes/random` — случайный рецепт
- `GET /recipes/random?include=tomato` — случайный рецепт с ингредиентами (можно указать match=all или match=any)
- `GET /health` — проверка что БД подключена

## Тестовые curl-команды

**Linux/Mac:**
```bash
curl http://localhost:5000/recipes
curl http://localhost:5000/recipes?has=egg,milk
curl -X POST http://localhost:5000/recipes -H "Content-Type: application/json" -d '{"title":"Ratatouille","ingredients":["eggplant","zucchini","tomato"],"steps":"step1"}'
curl http://localhost:5000/recipes/random?include=tomato
``` 

**Windows (PowerShell):**
Через экранирование кавычек
```powershell
curl.exe -X POST http://localhost:5000/recipes -H "Content-Type: application/json" -d '{\"title\":\"Ratatouille\",\"ingredients\":[\"eggplant\",\"zucchini\",\"tomato\"],\"steps\":\"step1\"}'
```
Или через Invoke-WebRequest
```powershell
$body = '{"title":"Ratatouille","ingredients":["eggplant","zucchini","tomato"],"steps":"step1"}'
Invoke-WebRequest -Uri http://localhost:5000/recipes -Method POST -ContentType "application/json" -Body $body
```

## Как устроено

- `app.py` — главный файл, здесь описаны все URL-адреса и обработчики запросов
- `database.py` — подключение к PostgreSQL через asyncpg (создание пула соединений и жизненный цикл приложения)
- `recipes.py` — функции для работы с рецептами (создание, поиск, фильтрация)

База данных запускается вместе с приложением через docker compose. Таблицы и тестовые данные создаются автоматически из `createDB.sql`.

## Технологии

- Python 3.11, FastAPI, uvicorn, Pydantic
- PostgreSQL 15 + asyncpg
- Docker Compose

## Любимые команды

```bash
# Запустить всё в фоне
docker compose up -d --build

# Остановить контейнеры
docker compose down

# Полная очистка проекта: -v (удаляет volumes) --rmi all удаляет все images
docker compose down -v --rmi all

# Удалить том с данными БД
docker volume rm vasilev_ryahov_postgres_data

# Показать таблицы в БД
docker compose exec db psql -U user -d recipes_db -c "\dt"

# Смотреть логи (-f логи в реальном времени -t видеть timestamps у каждой строки)
docker compose logs -f -t
```