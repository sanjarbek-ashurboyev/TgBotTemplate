FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy the manifest alone first so dependency layers survive source edits.
COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install .

COPY bot ./bot
COPY migrations ./migrations
COPY alembic.ini ./

# Never run as root inside the container.
RUN useradd --create-home --uid 1000 app && chown -R app:app /app
USER app

CMD ["python", "-m", "bot.main"]
