# Dockerfile
FROM python:3.11-slim

# System deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ui.html ./

ENV PG_HOST=host.docker.internal \
    PG_PORT=5432 \
    PG_DB=postgres \
    PG_USER=postgres \
    PG_PASS=postgres \
    HARD_ROW_LIMIT=5000 \
    STATEMENT_TIMEOUT_SECONDS=30 \
    ALLOW_DDL=false

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
