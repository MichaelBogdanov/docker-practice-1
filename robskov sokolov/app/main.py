from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()
topics = {}
topic_id = 0

class Topic(BaseModel):
    title: str

class Message(BaseModel):
    author: str
    text: str

@app.post("/topics")
def create_topic(topic: Topic):
    global topic_id
    topic_id += 1
    topics[topic_id] = {"id": topic_id, "title": topic.title, "messages": []}
    return topics[topic_id]

@app.post("/topics/{topic_id}/messages")
def create_message(topic_id: int, message: Message):
    topics[topic_id]["messages"].append(message.dict())
    return message

@app.get("/topics/{topic_id}/messages")
def get_messages(topic_id: int):
    return topics[topic_id]["messages"]