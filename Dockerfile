FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
