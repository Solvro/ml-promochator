#!/bin/bash

set -euo pipefail

if [ "$INITIALIZE_DATABASE" = "true"]; then
    echo "Initializing database..."
    python app/prestart.py
    alembic upgrade head
    python app/init_db.py
else
    echo "Not initializing database..."
fi

uvicorn app.main:app --port 8000 --host 0.0.0.0 --reload