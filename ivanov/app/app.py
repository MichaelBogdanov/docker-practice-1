from flask import Flask
import sqlite3
import json
from datetime import datetime

# ==== Конфигурация ==== #
DEBUG = True
PORT = 5000
DATABASE_PATH = 'weater_reposts.db'
# ==== Конфигурация ==== #

# Создаём приложение
app = Flask(__name__)

# Маршрутизация
# TODO

# Запускаем приложение
if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)