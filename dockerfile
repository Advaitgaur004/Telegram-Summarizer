FROM python:3.9-slim

# We don't need Ollama in the container since we'll use the host's instance

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY config.example.ini config.ini
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# No need to expose port 11434 as we'll use the host's Ollama

ENTRYPOINT ["/app/entrypoint.sh"]