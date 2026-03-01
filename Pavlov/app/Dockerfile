FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DB_HOST=db \
    DB_NAME=postgres \
    DB_USER=postgres \
    DB_PASSWORD=mysecretpassword

CMD ["python", "app.py"]