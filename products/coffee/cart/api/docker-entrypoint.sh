#!/bin/sh
set -e

. .venv/bin/activate
uvicorn cart.main:app --host 0.0.0.0 --port 8080 --no-access-log
