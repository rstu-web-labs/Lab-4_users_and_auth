FROM python:3.11-alpine
RUN apk update && apk add  gcc libffi-dev g++ py-pip --no-cache cargo gettext
WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && pip install "poetry==1.5.1" && poetry config virtualenvs.create false && poetry install --no-cache
RUN pip install uvicorn

RUN pip install secure-smtplib
RUN pip install celery

RUN pip install pydantic

RUN pip install alembic
RUN pip install psycopg2-binary

RUN pip install pydantic[email]
RUN pip install pandas

COPY ./app ./app

COPY alembic.ini ./
COPY migrations ./migrations

COPY config.py ./
