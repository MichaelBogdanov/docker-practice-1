# API для управления рецептами

## Запуск проекта

```bash
docker-compose up --build

curl -X POST http://localhost:5000/recipes -H "Content-Type: application/json" -d "{\"title\":\"Омлет\",\"ingredients\":[\"яйца\",\"молоко\"],\"steps\":\"Взбить и пожарить\"}"

curl "http://localhost:5000/recipes?has=яйца,молоко"

curl "http://localhost:5000/recipes/random?include=помидор"

