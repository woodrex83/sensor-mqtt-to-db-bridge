FROM python:3.11-slim AS stage

RUN apt-get update && \
    apt-get install build-essential curl gcc -y && \
    rm -rf /var/lib/apt/lists/*

# install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /usr/src/app

ADD . .

RUN poetry install --no-root --only main

ENTRYPOINT [ "poetry","run", "python", "-m" , "src.main" ]