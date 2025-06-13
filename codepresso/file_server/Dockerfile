FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    awscli curl && \
    pip install --no-cache-dir fastapi uvicorn

# Create a non-root user
RUN useradd -u 1000 appuser
USER appuser

WORKDIR /app
COPY main.py .

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
