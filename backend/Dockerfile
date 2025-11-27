FROM python:3.12-slim
WORKDIR /backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-traditional \
    build-essential \
    libpq-dev \
    gcc \
    postgresql-client \ 
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv --copies $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    echo "--- Venv packages installed: ---" && \
    pip list # Add this line to list installed packages during build

COPY ./entrypoint.sh /backend/entrypoint.sh
COPY ./seed_exercises.sql /backend/seed_exercises.sql
COPY . .

RUN chmod +x /backend/entrypoint.sh

ENTRYPOINT ["/backend/entrypoint.sh"]
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]