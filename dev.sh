#!/bin/bash
trap 'kill 0' EXIT

(cd api_extern && docker compose up --build) &
(cd backoffice && python3 app.py) &
(cd product_mcp_server && source venv/bin/activate && uvicorn app:app --host 0.0.0.0 --port 8000 --reload) &
(cd client_web && python3 -m http.server 8080) &

wait
