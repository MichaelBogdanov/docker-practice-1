# Работа с Docker и создание API

В рамках проекта реализованы три простых HTTP API-сервиса на **Python (Flask)**.
Каждый сервис контейнеризирован с помощью **Docker** и запускается через **docker-compose**.

Цель проекта — продемонстрировать базовые принципы разработки API и контейнеризации приложений.

---

# Архитектура проекта

Проект состоит из трёх независимых сервисов:

| Сервис         | Назначение                               | Порт |
| -------------- | ---------------------------------------- | ---- |
| URL Shortener  | сокращение ссылок и статистика переходов | 5000 |
| Image Metadata | хранение метаданных изображений          | 5001 |
| Recipes API    | база рецептов и поиск по ингредиентам    | 5002 |

Все сервисы запускаются одной командой через `docker-compose`.

---

# Запуск проекта

В корневой директории проекта выполнить:

```
docker compose up --build
```

После запуска сервисы будут доступны по адресам:

```
http://localhost:5000
http://localhost:5001
http://localhost:5002
```

---

# API 1 — URL Shortener

Сервис сокращает ссылки и ведёт статистику переходов.

### Основные endpoint’ы

**POST /shorten** — создание короткой ссылки

```
curl -X POST http://localhost:5000/shorten \
-H "Content-Type: application/json" \
-d '{"url":"https://example.com"}'
```

**GET /r/{code}** — редирект на оригинальную ссылку

```
curl -v http://localhost:5000/r/a1b2
```

**GET /stats/{code}** — статистика ссылки

```
curl http://localhost:5000/stats/a1b2
```

---

# API 2 — Image Metadata

Сервис хранит метаданные изображений:

* URL
* ширину
* высоту
* теги

### Endpoint’ы

**POST /images** — добавление изображения

```
curl -X POST http://localhost:5001/images \
-H "Content-Type: application/json" \
-d '{"url":"https://example.com/image.jpg","width":800,"height":600,"tags":["landscape"]}'
```

**GET /images** — список изображений

```
curl http://localhost:5001/images
```

**GET /images?tag=landscape** — фильтр по тегу

```
curl http://localhost:5001/images?tag=landscape
```

**GET /images/{id}** — детали изображения

```
curl http://localhost:5001/images/1
```

---

# API 3 — Recipes

Сервис представляет собой простую базу рецептов.

Каждый рецепт содержит:

* название
* ингредиенты
* шаги приготовления

### Endpoint’ы

**POST /recipes** — создать рецепт

```
curl -X POST http://localhost:5002/recipes \
-H "Content-Type: application/json" \
-d '{"title":"Ratatouille","ingredients":["eggplant","zucchini","tomato"],"steps":"Cut vegetables and bake them"}'
```

**GET /recipes** — список рецептов

```
curl http://localhost:5002/recipes
```

**GET /recipes?has=egg,milk** — поиск по ингредиентам

```
curl http://localhost:5002/recipes?has=egg,milk
```

**GET /recipes/random** — случайный рецепт

```
curl http://localhost:5002/recipes/random
```

**GET /recipes/random?include=tomato** — случайный рецепт с указанным ингредиентом

```
curl http://localhost:5002/recipes/random?include=tomato
```

---

# Реализованные решения

* Каждый API реализован как отдельный сервис на **Flask**
* Все сервисы контейнеризированы с помощью **Docker**
* Для запуска используется **docker-compose**
* Данные хранятся **в памяти приложения**, что упрощает реализацию
* Все сервисы можно протестировать через **curl**

---

# Вывод

В проекте реализованы три независимых HTTP API-сервиса, которые демонстрируют основы разработки REST API и контейнеризации приложений с помощью Docker.
