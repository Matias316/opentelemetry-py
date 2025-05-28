# Use official Python image
FROM python:3.11-slim

# Set env vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.2

RUN apt-get update \
    && apt-get install -y curl build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && apt-get clean

# Set workdir
WORKDIR /app

# Copy files
COPY pyproject.toml poetry.lock ./

# Install dependencies (no virtualenv inside Docker)
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi \
    && poetry run pip install opentelemetry-distro opentelemetry-exporter-otlp gunicorn

# Copy rest of the code
COPY . .

# Expose port Flask will run on
EXPOSE 8080

# Set OpenTelemetry environment variables
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_LOGS_EXPORTER=otlp
ENV OTEL_METRICS_EXPORTER=none
ENV OTEL_EXPORTER_OTLP_ENDPOINT=grpc://otel-collector:4317
ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc
ENV OTEL_EXPORTER_OTLP_INSECURE=true

# Run using instrumed gunicorn
CMD ["poetry", "run", "opentelemetry-instrument", "--logs_exporter", "otlp", "gunicorn", "-w", "3", "-b", "0.0.0.0:8080", "--timeout", "120", "app.app:app"]
