# Задача 08 — Метаданные картинок

# Участники группы
Темнева А.Р.

# Описание решения
Flask-приложение хранит мета-информацию об изображениях (url, width, height, tags).
Данные хранятся в памяти. Поддерживается фильтрация по тегам.

# Как запустить
docker compose up --build

# Тестовые curl-команды и результат
1 curl http://localhost:5000/images - пустой список []
2 curl http://localhost:5000/images?tag=portrait - фильтр по несуществующему тегу, вывело []
3 curl -X POST http://localhost:5000/images -H "Content-Type: application/json" -d '{"url":"https://...","width":800,"height":600,"tags":["landscape"]}' - добавление изображения, выводит как раз добавленное изображение в {}
4 curl http://localhost:5000/images/1 - получение по id

после заполнения:
1 curl http://localhost:5000/images?tag=landscape - фильтр по существующему тегу, выводит добавленное изображение в {}
2 curl http://localhost:5000/images - список всех изображений, после команд выводит добавленное