FROM python:3.10-slim AS base

ENV PYTHONUNBUFFERED=1

WORKDIR /promochator

ENV PYTHONPATH=/promochator

COPY ./pyproject.toml /promochator/pyproject.toml

# Development stage
FROM base AS development
RUN echo "Installing packages..."
RUN pip install --upgrade pip
RUN pip install --no-cache-dir .[dev]

COPY ./data /promochator/data

COPY ./config /promochator/config

COPY ./playground /promochator/playground

COPY ./Makefile /promochator/Makefile 

COPY ./app /promochator/app

COPY ./alembic.ini /promochator/alembic.ini

COPY ./entrypoint.sh /promochator/entrypoint.sh

EXPOSE 8000

RUN echo "Service is ready to run in development mode"
ENTRYPOINT ["bash", "./entrypoint.sh"]

# Production stage
FROM base AS production
RUN echo "Installing packages..."
RUN pip install --upgrade pip
RUN pip install --no-cache-dir .

COPY ./data /promochator/data

COPY ./config /promochator/config

COPY ./app /promochator/app

COPY ./alembic.ini /promochator/alembic.ini

COPY ./entrypoint.sh /promochator/entrypoint.sh

EXPOSE 8000

RUN echo "Running app..."
ENTRYPOINT ["bash", "./entrypoint.sh"]