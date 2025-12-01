# docker/backend.Dockerfile
FROM python:3.12-slim AS backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 시스템 패키지 (psycopg 등 빌드용)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Poetry + 의존성 설치
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --only main

# 나머지 프로젝트 복사
COPY . .

# (필요하면) static 모아서 쓰고 싶을 때
# RUN python manage.py collectstatic --noinput

# gunicorn으로 서비스 실행
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
