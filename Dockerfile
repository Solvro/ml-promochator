FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

CMD ["uvicorn", "--proxy-headers", "--forwarded-allow-ips", "127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16", "main:app", "--host", "0.0.0.0", "--port", "8000"]
