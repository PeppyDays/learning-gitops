#!/bin/sh
set -e

. .venv/bin/activate
uvicorn order.main:app --host 0.0.0.0 --port 8080 --no-access-log
