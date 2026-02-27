# Первая практическая работа по работе с Docker

Вам необходимо сделать форк (```fork```) данного репозитория на свой аккаунт GitHub и клонировать (```clone```) его на свой локальный компьютер.

После клонирования форка, скачайте из релизов (```Releases```) программу, выдающую номер задания по номеру академической группы и Вашим фамилиям.
> ***Обратите внимание, некорректный ввод в программу, а вследствие и неправильный номер задания, исключительно на Вашей ответственности. Решение не Вашего задания проверяться не будет.***

После получения номера задания, найдите его ниже и приступайте к выполнению в ранее клонированном репозитории на любом удобном Вам языке программирования, создавая коммиты (```commit```) по смысловым шагам.

В рамках данного задания вам предстоит разработать и контейнеризовать простой ```HTTP API```. Каждый из Вас получил описание конкретного API: его назначение, список поддерживаемых endpoint’ов и примеры HTTP-запросов. На основе этого описания необходимо самостоятельно реализовать серверное приложение, которое корректно обрабатывает указанные запросы, возвращает ожидаемые ответы и хранит данные. Точная внутренняя реализация остаётся на Ваше усмотрение, при условии соблюдения заданного API-контракта.

После реализации приложения требуется упаковать его в Docker-контейнер и настроить запуск через ```docker compose```. В результате проект должен запускаться одной командой, автоматически поднимая все необходимые сервисы (приложение, базу данных и т.д.). Работоспособность API должна подтверждаться выполнением тестовых ```curl```-запросов, приведённых в описании задания. Дополнительно необходимо подготовить краткий ```README``` с описанием реализованных решений. Основная цель задания - освоить базовые принципы контейнеризации, работы с Docker и проектирования простых API, а не реализация сложной бизнес-логики.

После завершения работы необходимо запушить ```push``` изменения в свой форк ```fork``` и сделать ```Pull Request``` в данный репозиторий.
> ***Обратите внимание, только после получения реквеста будет считаться, что Вы сдали работу. Работа может быть не принята по ряду причин, в таком случае подробную информацию об этом я напишу в комментариях к запросу.***

## Общие инструкции

1. Убедитесь, что Docker Desktop установлен и запущен.
2. В папке проекта, названной фамилией(ями) выполняющих работу студентов (например, ```bogdanov_zanin```), должен быть `docker-compose.yml` и каталог `app`.

Пример требуемой структуры репозитория:
```
<имена студентов>/   ← папка (например, bogdanov_zanin)
  app/
    app.py
    requirements.txt
    Dockerfile
  README.md          ← описание реализованных решений
  docker-compose.yml
```

3. Сборка и запуск:

```powershell
docker compose up --build
```

***Запуск проекта при проверке будет осуществлён именно данной командой в корне проекта.***

4. По умолчанию API слушают `http://localhost:5000/` (если требуется - укажите порт в `docker-compose.yml`).

## Задания
<details>
<summary>1) Цитатник</summary>

**Описание:** хранилище коротких цитат с возможностью фильтрации по тегу и получения случайной цитаты.

**Endpoints:**

* `GET /quotes` - список (опционально `?tag=life&limit=10`)
* `GET /quotes/random` - случайная цитата (`?tag=...`)
* `POST /quotes` - добавить `{ "text": "...", "author": "...", "tags": ["..."] }`
* `DELETE /quotes/{id}` - удалить

**Тестовые curl-команды:**

```bash
curl http://localhost:5000/quotes
curl http://localhost:5000/quotes?tag=life
curl http://localhost:5000/quotes/random
curl -X POST http://localhost:5000/quotes -H "Content-Type: application/json" -d '{"text":"Wake the F-word up, Samurai! We have a city to burn!","author":"Johnny Silverhand","tags":["life","motivation"]}'
curl -X DELETE http://localhost:5000/quotes/1
```
</details>

<details>
<summary>2) TODO</summary>

**Описание:** простой TODO с приоритетом, сроками и статусами.

**Endpoints:**

* `GET /tasks` - список (`?status=open&priority=1`)
* `POST /tasks` - создать `{ "title":"...", "due":"YYYY-MM-DD", "priority":1 }`
* `PATCH /tasks/{id}` - обновить `{ "status":"done" }`
* `DELETE /tasks/{id}`

**Тестовые curl-команды:**

```bash
curl http://localhost:5000/tasks
curl http://localhost:5000/tasks?status=open
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title":"Принять красную таблетку","due":"1998-02-19","priority":1}'
curl -X PATCH http://localhost:5000/tasks/1 -H "Content-Type: application/json" -d '{"status":"done"}'
curl -X DELETE http://localhost:5000/tasks/1
```
</details>

<details>
<summary>3) Шутки (анекдоты)</summary>

**Описание:** шутки по категориям с возможностью голосовать `up`/`down`.

**Endpoints:**

* `GET /jokes` - список (`?category=programming`)
* `GET /jokes/random` - случайная (`?category=math`)
* `POST /jokes` - добавить `{ "text":"...", "category":"..." }`
* `POST /jokes/{id}/vote` - `{ "vote":"up" }`

**Тестовые curl-команды:**

```bash
curl http://localhost:5000/jokes
curl http://localhost:5000/jokes?category=programming
curl http://localhost:5000/jokes/random
curl -X POST http://localhost:5000/jokes -H "Content-Type: application/json" -d '{"text":"Knock knock. Who'\''s there? Woo. Woo who? That'\''s the sound of da Police!","category":"cops"}'
curl -X POST http://localhost:5000/jokes/1/vote -H "Content-Type: application/json" -d '{"vote":"up"}'
```
</details>

<details>
<summary>4) Трекер привычек</summary>

**Описание:** отмечаем выполнение привычек по датам, считаем текущую серию `streak`.

**Endpoints:**

* `POST /habits` - `{ "name":"Пробежка", "user_id":1 }`
* `POST /habits/{id}/check` - `{ "date":"YYYY-MM-DD" }`
* `GET /habits/{id}/streak` - возвращает число дней подряд

**Тестовые curl-команды:**

```bash
curl http://localhost:5000/habits
curl -X POST http://localhost:5000/habits -H "Content-Type: application/json" -d '{"name":"Пробежка","user_id":1}'
curl -X POST http://localhost:5000/habits/1/check -H "Content-Type: application/json" -d '{"date":"2026-02-27"}'
curl http://localhost:5000/habits/1/streak
```
</details>

<details>
<summary>5) Сервис коротких ссылок</summary>

**Описание:** сокращение URL и редирект по коду.

**Endpoints:**

* `POST /shorten` - `{ "url":"https://..." }` → `{ "code":"a1b2" }`
* `GET /r/{code}` - 302 редирект
* `GET /stats/{code}` - просмотры и дата создания

**Тестовые curl-команды:**

```bash
curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
curl -v http://localhost:5000/r/a1b2
curl http://localhost:5000/stats/a1b2
```
</details>

<details>
<summary>6) Местные заметки о погоде</summary>

**Описание:** короткие пользовательские заметки о погоде в городе.

**Endpoints:**

* `POST /reports` - `{ "city":"ttp://localhost:5000/reports?city=moscow","text":"sunny","temp":12 }`
* `GET /reports` - список (`?city=Великий%20Новгород`)
* `GET /reports/recent` - последние N записей

**Тестовые curl-команды:**

```bash
curl http://localhost:5000/reports
curl http://localhost:5000/reports?city=moscow
curl -X POST http://localhost:5000/reports -H "Content-Type: application/json" -d '{"city":"moscow","text":"sunny","temp":12}'
curl http://localhost:5000/reports/recent
```
</details>

<details>
<summary>7) Доска сообщений</summary>

**Описание:** темы и сообщения в них (топики).

**Endpoints:**

* `POST /topics` - `{ "title":"..." }`
* `POST /topics/{id}/messages` - `{ "author":"...","text":"..." }`
* `GET /topics/{id}/messages` - список сообщений

**Тестовые curl-команды:**

```bash
curl http://localhost:5000/topics
curl -X POST http://localhost:5000/topics -H "Content-Type: application/json" -d '{"title":"Замедление и возможная блокировка Telegram"}'
curl -X POST http://localhost:5000/topics/1/messages -H "Content-Type: application/json" -d '{"author":"Неизвестный","text":"Все уже скачали MAX?"}'
curl http://localhost:5000/topics/1/messages
```
</details>

<details>
<summary>8) Метаданные картинок</summary>

**Описание:** храним только мета-информацию о изображениях (url, tags, width, height).

**Endpoints:**

* `POST /images` - `{ "url":"...","width":800,"height":600,"tags":["..."] }`
* `GET /images` - фильтр по тегу `?tag=landscape`
* `GET /images/{id}` - детали

**Тестовые curl-команды:**

```bash
curl http://localhost:5000/images
curl http://localhost:5000/images?tag=portrait
curl -X POST http://localhost:5000/images -H "Content-Type: application/json" -d '{"url":"https://...","width":800,"height":600,"tags":["landscape"]}'
curl http://localhost:5000/images/1
```
</details>

<details>
<summary>9) Таблица рекордов</summary>

**Описание:** топ по очкам для разных игр.

**Endpoints:**

* `POST /scores` - `{ "player":"madmax","game":"digdug","score":751300 }`
* `GET /scores/top` - `?game=digdug&limit=10`
* `GET /scores/player/{name}` - личные результаты

**Тестовые curl-команды:**

```bash
curl http://localhost:5000/scores/top?game=digdug&limit=5
curl -X POST http://localhost:5000/scores -H "Content-Type: application/json" -d '{ "player":"madmax","game":"digdug","score":751300}'
curl http://localhost:5000/scores/player/Misha
```
</details>

<details>
<summary>10) Рецепты</summary>

**Описание:** база рецептов; поиск по имеющимся ингредиентам.

**Endpoints:**

* `POST /recipes` - `{ "title":"Ratatouille","ingredients":["eggplant","zucchini", "..."],"steps":"..." }`
* `GET /recipes` - `?has=egg,milk`
* `GET /recipes/random` - `?include=tomato`

**Тестовые curl-команды:**

```bash
curl http://localhost:5000/recipes
curl http://localhost:5000/recipes?has=egg,milk
curl -X POST http://localhost:5000/recipes -H "Content-Type: application/json" -d '{"title":"Ratatouille","ingredients":["eggplant","zucchini", "..."],"steps":"..."}'
curl http://localhost:5000/recipes/random?include=tomato
```
</details>

<details>
<summary>11) Полив растений</summary>

**Описание:** виртуальный горшок - отмечаем полив и получаем статус.

**Endpoints:**

* `POST /plants` - `{ "name":"ficus","water_interval_days":7 }`
* `POST /plants/{id}/water` - `{ "date":"YYYY-MM-DD" }`
* `GET /plants/{id}/status` - `{ "days_since_water": 3, "need_water": true }`

**Тестовые curl-команды:**

```bash
curl http://localhost:5000/plants
curl -X POST http://localhost:5000/plants -H "Content-Type: application/json" -d '{"name":"ficus","water_interval_days":7}'
curl -X POST http://localhost:5000/plants/1/water -H "Content-Type: application/json" -d '{"date":"2026-02-27"}'
curl http://localhost:5000/plants/1/status
```
</details>

<details>
<summary>12) Список фильмов</summary>

**Описание:** список фильмов к просмотру со статусами и оценками.

**Endpoints:**

* `POST /movies` - `{ "title":"Начало","year":2010 }`
* `PATCH /movies/{id}` - `{ "status":"watched","rating":9 }`
* `GET /movies` - `?status=to-watch`

**Тестовые curl-команды:**

```bash
curl http://localhost:5000/movies
curl -X POST http://localhost:5000/movies -H "Content-Type: application/json" -d '{"title":"Начало","year":2010}'
curl -X PATCH http://localhost:5000/movies/1 -H "Content-Type: application/json" -d '{"status":"watched","rating":9}'
curl http://localhost:5000/movies?status=to-watch
```
</details>
