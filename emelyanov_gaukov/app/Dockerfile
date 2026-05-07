FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN mkdir -p /data
ENV PORT=5000
ENV DATA_FILE=/data/links.json
EXPOSE 5000
CMD ["python", "app.py"]