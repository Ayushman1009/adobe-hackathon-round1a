
FROM --platform=linux/amd64 python:3.9-slim-buster

WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir --compile -r requirements.txt


COPY src/ ./src/


COPY input/ ./input/


CMD ["python", "src/main.py"]
