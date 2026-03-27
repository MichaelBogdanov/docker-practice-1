@echo off
chcp 65001

echo //////////Цитатник////////////

echo ========== GET Все ==========
echo http://localhost:8000/quotes/
curl -L -i http://localhost:8000/quotes/

echo ========== GET Цитата с тегом motivation  ==========
echo http://localhost:8000/quotes?tag=motivation
curl -L -i http://localhost:8000/quotes?tag=motivation

echo ========== GET Случайная цитата ==========
echo GET http://localhost:8000/quotes/random
curl -i http://localhost:8000/quotes/random

echo ========== POST Новая цитата ==========
echo POST http://localhost:8000/quotes/
curl -L -i -X POST http://localhost:8000/quotes/ ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Wake the F-word up, Samurai! We have a city to burn!\",\"author\":\"Johnny Silverhand\",\"tags\":[\"life\",\"motivation\"]}"

echo ========== DELETE Удалить цитату с id = 1 ==========
curl -i -X DELETE http://localhost:8000/quotes/1

echo //////////Трекер привычек////////////

echo \n ========== GET Все привычки ==========
echo http://localhost:8000/habits
curl -L -i http://localhost:8000/habits

echo ========== POST Новая привычка ==========
echo POST http://localhost:8000/habits
curl -L -i -X POST http://localhost:8000/habits ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Пробежка\",\"user_id\":1}"

echo ========== POST Отметка о выполнении для привычки 1 ==========
echo POST http://localhost:8000/habits/1/check
curl -L -i -X POST http://localhost:8000/habits/1/check ^
  -H "Content-Type: application/json" ^
  -d "{\"date\":\"2026-02-27\"}"

echo ========== GET Текущая серия streak для привычки 1 ==========
echo GET http://localhost:8000/habits/1/streak
curl -L -i http://localhost:8000/habits/1/streak

echo ========== GET Все привычки после добавления ==========
echo http://localhost:8000/habits
curl -L -i http://localhost:8000/habits
pause