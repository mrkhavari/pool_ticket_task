FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /src

COPY pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry==1.6 && \
    poetry config virtualenvs.in-project true && \
    poetry install --only main

COPY ./app ./app
COPY ./alembic.ini ./alembic.ini

RUN mkdir ./logs

CMD export APP_VERSION=`poetry version -s` && \
    poetry run alembic upgrade head && \
    poetry run uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 8000