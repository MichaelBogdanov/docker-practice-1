# TODO API (Flask + Docker)

Простой HTTP API для управления списком задач (TODO) с приоритетом, сроком и статусом.  
Приложение реализовано на *Flask* и упаковано в Docker, запуск осуществляется через `docker compose`.

## Что делает API

API позволяет:

* получать список задач, в том числе с фильтрацией по статусу и приоритету;
* создавать новую задачу с названием (`title`), сроком (`due`) и приоритетом (`priority`);
* изменять статус задачи (`status`);
* удалять задачу по её идентификатору (`id`).

Данные хранятся в памяти процесса (список `tasks`), поэтому при перезапуске контейнера очищаются — для учебного задания этого достаточно.

## Как запустить

### Требования

* установлен и запущен Docker Desktop.

### Команды

В корне папки с проектом:

`docker compose up --build`

### Примеры запросов

Посмотреть задачи:
`curl http://localhost:5000/tasks`

Добавление задачи:
`curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Take red pill\",\"due\":\"1998-02-19\",\"priority\":1}"`

Посмотреть задачи со статусом open:
`curl "http://localhost:5000/tasks?status=open"`

Изменить статус задачи:
`curl -X PATCH http://localhost:5000/tasks/3 -H "Content-Type: application/json" -d "{\"status\":\"done\"}"`

Удалить задачу:
`curl -X DELETE http://localhost:5000/tasks/2`
