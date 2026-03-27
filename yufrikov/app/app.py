from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import os

app = FastAPI()

# получаем подключение к базе
def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ.get("DB_NAME", "board"),
        user=os.environ.get("DB_USER", "user"),
        password=os.environ.get("DB_PASSWORD", "password"),
    )

# создаем таблицы в первый раз
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        create table if not exists topics (
            id serial primary key,
            title text not null
        );
        create table if not exists messages (
            id serial primary key,
            topic_id integer references topics(id),
            author text not null,
            text text not null
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


init_db()

# модели 
class TopicIn(BaseModel):
    title: str


class MessageIn(BaseModel):
    author: str
    text: str


# просмотр тем
@app.get("/topics")
def list_topics():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("select * from topics order by id")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in result]


# запись тем
@app.post("/topics", status_code=201)
def create_topic(data: TopicIn):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("insert into topics (title) values (%s) returning *", (data.title,))
    topic = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return dict(topic)


# получение сообщение определенной темы по id 
@app.get("/topics/{topic_id}/messages")
def list_messages(topic_id: int):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("select * from messages where topic_id = %s order by id", (topic_id,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in result]


# запись сообщение определенной темы по id 
@app.post("/topics/{topic_id}/messages", status_code=201)
def create_message(topic_id: int, data: MessageIn):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "insert into messages (topic_id, author, text) values (%s, %s, %s) returning *",
        (topic_id, data.author, data.text)
    )
    message = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return dict(message)