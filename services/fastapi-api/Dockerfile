FROM python:3.9.7-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED True
ENV POETRY_VERSION=1.1.12

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION
ENV PATH="/root/.local/bin:$PATH"

# Copy project specification and install deps
COPY poetry.lock* pyproject.toml /
RUN poetry config virtualenvs.create false && cd / && poetry install

COPY format.sh lint.sh test.sh /scripts/
COPY ./app /app

ENV PYTHONPATH=/app

CMD ["uvicorn", "fastapi_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
