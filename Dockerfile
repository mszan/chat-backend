# pull official base image
FROM python:3.7.6-alpine

# prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements requirements

RUN \
  # pip install --upgrade pip && \
  # apk add --no-cache postgresql-libs && \
  apk add --no-cache \
    musl-dev \
    libffi-dev \
    gcc \
    postgresql-dev \
    libressl-dev \
    musl-dev \
    && \
  pip install -r requirements/dev.txt --no-cache-dir
  # apk --purge del .build-deps

COPY . .
