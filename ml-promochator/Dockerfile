FROM python:3.10-slim AS base

WORKDIR /app/

COPY ./pyproject.toml /backend/pyproject.toml

# Development stage
FROM base AS development
RUN echo "Installing packages..."
RUN pip install --upgrade pip
RUN pip install --no-cache-dir .[dev]

COPY ./config/ /app/

COPY ./playground/ /app/

COPY ./Makefile /app/

COPY ./app /app/app

EXPOSE 8000 8888

RUN echo "Service is ready to run in development mode"

# Production stage
FROM base AS production
RUN echo "Installing packages..."
RUN pip install --upgrade pip
RUN pip install --no-cache-dir .

COPY ./config/ /app/

COPY ./app /app/app

EXPOSE 8000

RUN echo "Running app..."
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]