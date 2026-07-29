# Product MCP Server

Ce dossier contient un service d'assistance IA dédié au catalogue produit de HBntory. Il combine trois briques principales :

- un serveur MCP exposant un outil pour interroger un catalogue externe,
- un agent IA basé sur LangGraph et Ollama,
- une API FastAPI permettant d'envoyer des questions depuis un front-end ou un client HTTP.

## Objectif

Le but de ce module est de permettre à un utilisateur de poser une question naturelle sur un produit, par exemple :

- “Donne-moi les détails du produit HB-LAP-1001”
- “Quel est le prix du produit X ?”

L'agent utilise alors l'outil MCP pour récupérer les informations depuis l'API externe du catalogue.

## Architecture

Le projet est organisé autour de trois fichiers principaux :

- [app.py](app.py) : API FastAPI qui reçoit les requêtes HTTP et retourne une réponse structurée.
- [agent.py](agent.py) : orchestration de l'agent ReAct avec LangGraph et Ollama, via un serveur MCP lancé en STDIO.
- [server.py](server.py) : serveur MCP qui expose l'outil de récupération des produits.

## Prérequis

Avant de démarrer, assurez-vous d'avoir :

- Python 3.10+
- un environnement virtuel Python
- Ollama installé et un modèle disponible (par exemple qwen2.5)
- l'API externe du catalogue accessible sur http://localhost:5001

## Installation

Depuis la racine du dossier :

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS / WSL
# ou : .\venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

## Variables d'environnement

Le serveur MCP peut utiliser la variable suivante :

- EXTERNAL_API_URL : URL de base de l'API externe du catalogue
  - valeur par défaut : http://localhost:5001

## Démarrage

### 1. Vérifier l'API externe

Assurez-vous que l'API du catalogue est bien disponible sur :

```text
http://localhost:5001
```

### 2. Vérifier Ollama

Assurez-vous que le modèle utilisé par l'agent est disponible, par exemple :

```bash
ollama run qwen2.5:1.5b
```

### 3. Lancer l'API FastAPI

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

L'API sera alors disponible sur :

```text
http://localhost:8000
```

## Utilisation de l'API

### Endpoint

```http
POST /ask
Content-Type: application/json
```

### Exemple de requête

```json
{
  "question": "Donne-moi les détails du produit HB-LAP-1001"
}
```

### Exemple de réponse

```json
{
  "answer": "Détails du produit du catalogue externe :\n- SKU : HB-LAP-1001\n- Nom : Portable Pro..."
}
```

## Structure du dossier

```text
product_mcp_server/
├── app.py
├── agent.py
├── server.py
├── requirements.txt
├── README.md
└── tests/
```

## Notes

- L'agent appelle l'outil MCP via STDIO.
- Les erreurs réseau ou d'API externe sont gérées de manière explicite pour éviter de faire planter l'application.
- En cas de problème, vérifiez d'abord la disponibilité de l'API externe et du service Ollama.
