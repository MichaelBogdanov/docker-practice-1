Сервис коротких ссылок - Дружинин Иван, Григорьев Илья - Группа 3992

Описание:
Данный сервис позволяет преобразовывать длинные URL-адреса в короткие уникальные коды. 
При переходе по короткой ссылке пользователь автоматически перенаправляется на исходный URL. 
Сервис также предоставляет статистику переходов по каждой созданной ссылке.

Инструкция по запуску:

1. Откройте терминал 

2. Перейти в папку с проектом
cd путь_к_папке/druzhinin_grigoryev

3. Запустите Docker Compose:
docker compose up --build

4. Проверка работоспособности:
curl http://localhost:5000/health

5. Тестирование:
C:\WINDOWS\system32>curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d "{\"url\":\"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"}"
Вывод:
{"code":"r0Pg"}

C:\WINDOWS\system32>curl -v http://localhost:5000/r/a1b2
Вывод:
<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">https://www.youtube.com/watch?v=dQw4w9WgXcQ</a>. If not, click the link.
* we are done reading and this is set to close, stop send
* abort upload
* shutting down connection #0

C:\WINDOWS\system32>curl http://localhost:5000/stats/r0Pg
{"code":"r0Pg","created_at":"2026-05-15T21:06:20.168159","original_url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ","views":1}