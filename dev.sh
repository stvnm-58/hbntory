#!/bin/bash
trap 'kill 0' EXIT

# api_extern n'a aucune dépendance externe (stdlib Python uniquement) : on le
# lance directement plutôt que via Docker, pour ne pas dépendre de
# l'intégration WSL de Docker Desktop. Port 5001 pour matcher
# Config.PRODUCT_API_URL (backoffice) et PRODUCT_API_URL (search_service).
(cd api_extern && HBN_PRODUCTS_PORT=5001 python3 app.py) &

# Ollama installé localement (sans sudo) sous ~/.local/ollama ; nécessaire
# pour l'agent de product_mcp_server (voir agent.py, modèle qwen2.5:1.5b).
export PATH="$HOME/.local/ollama/bin:$PATH"
export OLLAMA_MODELS="$HOME/.local/ollama/models"
ollama serve &

(cd backoffice && source venv/bin/activate && python3 app.py) &
(cd product_mcp_server && source venv/bin/activate && uvicorn app:app --host 0.0.0.0 --port 8000 --reload) &
(cd client_web && python3 -m http.server 8080) &

wait
