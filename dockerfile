FROM python:3.9-slim

RUN apt-get update && apt-get install -y curl
RUN curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/local/bin/ollama && \
    chmod +x /usr/local/bin/ollama

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY config.ini.example config.ini
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 11434

ENTRYPOINT ["/app/entrypoint.sh"]