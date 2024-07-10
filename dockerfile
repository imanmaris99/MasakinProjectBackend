# Use the official Python image with version 3.8
FROM python:3.8

# Install dependencies required for psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y \
       libpq-dev \
       gcc \
       python3-dev \
       build-essential \
       && rm -rf /var/lib/apt/lists/*

# Install Poetry (dependency manager)
RUN pip3 install poetry

# Set environment variables for Poetry
ENV POETRY_NO_INTERACTION=1 \
       POETRY_VIRTUALENVS_IN_PROJECT=1 \
       POETRY_VIRTUALENVS_CREATE=1 \
       POETRY_CACHE_DIR=/tmp/poetry_cache

# Set environment variables for Flask and database
ENV . app/.env

# Set the working directory inside the container
WORKDIR /app

# Copy pyproject.toml and poetry.lock* into the container
COPY pyproject.toml poetry.lock* /app/

# Install dependencies using Poetry
RUN poetry install

# Copy the entire project directory into the container
COPY . /app

# exposing Docker Port
EXPOSE 5001

# Specify the default command to run the application
# CMD ["/app/.venv/bin/gunicorn", "-w 4", "-b 0.0.0.0", --port=5000,"app:app"]
CMD poetry run flask run --host=0.0.0.0 --port=5000
