# Secure Cloud DevSecOps Platform

A learning project for building and securing a cloud-hosted application using DevSecOps practices.

## Current Features

- FastAPI backend
- PostgreSQL database
- `GET /health`
- `GET /users`
- `POST /users`
- Automated tests with pytest

## Run Locally

Activate the virtual environment:

    source .venv/bin/activate

Set the database connection:

    export DATABASE_URL="postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE"

Start the API:

    python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

Run tests:

    python -m pytest