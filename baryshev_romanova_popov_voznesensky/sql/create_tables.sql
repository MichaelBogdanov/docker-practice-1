CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    author VARCHAR NOT NULL,
    tags TEXT[] NOT NULL DEFAULT '{}'
);

-- Мне лень реализовывать таблицу users 🙏
CREATE TABLE habits (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    user_id INTEGER NOT NULL 
);

CREATE TABLE habit_checks (
    id SERIAL PRIMARY KEY,
    habit_id INTEGER NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    CONSTRAINT uix_habit_date UNIQUE (habit_id, date)
);