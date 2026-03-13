# Docker Practice 1 — Выполнили Кириллов С.В и Спиридонов М.О 2991

## Описание проекта
Проект реализует три API-сервиса на Flask и запускается в Docker desk через `docker-compose`:

1. **Jokes API** (3 задание - шутки по категориям с возможностью голосовать)  
2. **Scores API** (9 задание - таблица рекордов для игр)  
3. **Plants API** (11 задание - отслеживание полива растений)

## Краткое решение API-запросов

### Jokes API (шутки)

```http
GET /jokes
# Возвращает список всех шуток

GET /jokes?category=programming
# Возвращает шутки по категории "programming"

GET /jokes/random
# Возвращает случайную шутку, можно фильтровать по категории

POST /jokes
Content-Type: application/json
{
  "text": "Текст шутки",
  "category": "programming"
}
# Добавляет новую шутку

POST /jokes/{id}/vote
Content-Type: application/json
{
  "vote": "up"
}
# Голосует за шутку (up/down)
```
### Scores API (Таблица рекордов)
```http
POST /scores
Content-Type: application/json
{
  "player": "madmax",
  "game": "digdug",
  "score": 751300
}
# Добавляет результат игрока

GET /scores/top?game=digdug&limit=10
# Возвращает топ 10 игроков по игре digdug

GET /scores/player/madmax
# Возвращает все результаты игрока "madmax"
```
### Plants API (Полив растений)
```http
POST /plants
Content-Type: application/json
{
  "name": "ficus",
  "water_interval_days": 7
}
# Добавляет растение

POST /plants/{id}/water
Content-Type: application/json
{
  "date": "YYYY-MM-DD"
}
# Отмечает полив растения

GET /plants/{id}/status
# Возвращает статус растения: количество дней с последнего полива и нужно ли поливать
```
### Примечания:

Все данные хранятся в памяти (Python-списки) и сбрасываются при перезапуске контейнера.

API запускается на http://localhost:5000/ и тестируется через curl