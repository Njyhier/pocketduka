FROM python:3.11-slim AS builder

WORKDIR /app

RUN python -m venv /opt/.venv

ENV PATH="/opt/.venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /opt/.venv /opt/.venv

ENV PATH="/opt/.venv/bin:$PATH"

COPY --from=builder /app /app

EXPOSE 8002

CMD ["gunicorn","-k","uvicorn.workers.UvicornWorker","app.app:app","--bind","0.0.0.0:8002"]
