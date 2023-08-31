FROM python:3.11-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random

WORKDIR /app

FROM base as package

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true && \
    poetry install --only=main --no-root --no-ansi

FROM package as builder

COPY README.md ./
COPY src ./src
RUN poetry build

FROM base as runner

COPY --from=package /app/.venv ./.venv
COPY --from=builder /app/dist .
COPY config.yaml ./
COPY docker-entrypoint.sh .

LABEL org.opencontainers.image.source=https://github.com/2mason/learning-gitops

RUN ./.venv/bin/pip install --no-cache-dir *.whl

CMD ["./docker-entrypoint.sh"]
