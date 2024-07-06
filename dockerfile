# Menggunakan image resmi Python slim dengan versi 3.12.1
FROM python:3.8

# Argument yang dapat diatur saat membangun image
ARG FLASK_DEBUG
ARG FLASK_ENV
ARG DATABASE_TYPE
ARG DATABASE_NAME
ARG DATABASE_HOST
ARG DATABASE_PORT
ARG DATABASE_USER
ARG DATABASE_PASSWORD

# Menginstal dependensi yang diperlukan untuk psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y \
       libpq-dev \
       gcc \
       && rm -rf /var/lib/apt/lists/*

# Menginstal poetry (manajer dependensi)
RUN pip3 install poetry

# Mengatur variabel lingkungan untuk poetry
ENV POETRY_NO_INTERACTION=1 \
       POETRY_VIRTUALENVS_IN_PROJECT=1 \
       POETRY_VIRTUALENVS_CREATE=1 \
       POETRY_CACHE_DIR=/tmp/poetry_cache

# Mengatur direktori kerja di dalam container
WORKDIR /app

# Menyalin file pyproject.toml dan poetry.lock* ke dalam container
COPY pyproject.toml poetry.lock* /app/

# Menginstal dependensi menggunakan Poetry
RUN poetry install

# Menyalin seluruh konten dari direktori proyek ke dalam container
COPY . /app

# Melakukan migrasi database (asumsi menggunakan Flask-Migrate)
RUN poetry run flask db upgrade

# Menentukan perintah default untuk menjalankan aplikasi
CMD ["/app/.venv/bin/gunicorn", "-w 4", "-b 0.0.0.0:5000", "app:app"]
