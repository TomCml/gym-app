FROM python:3.12-slim
WORKDIR /backend
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser/backend
RUN python -m venv venv
COPY --chown=appuser:appuser requirements.txt ./
RUN venv/bin/pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser:appuser . .
EXPOSE 8000
CMD ["venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]