# 📦 Serveur MCP & Agent IA - Catalogue Produits

Ce module fournit un agent IA (LangChain/LangGraph + Ollama) interconnecté via le protocole MCP (Model Context Protocol) à une API externe pour interroger le catalogue produit.

---

## 🛠️ PRÉREQUIS

Avant de commencer, assure-toi d'avoir installé sur ta machine :

* **Python 3.10+**
* **Docker** (pour exécuter l'API externe du catalogue)
* **Ollama** (avec le modèle **Qwen** téléchargé)

---

## 🚀 INSTALLATION & DÉMARRAGE RAPIDE

### 1. Récupérer le code à jour

`git pull origin main`  
`cd product_mcp_server`

### 2. Configurer l'environnement virtuel Python

Créer le venv (si ce n'est pas déjà fait) :  
`python3 -m venv venv`

Activer le venv :  
* Linux / WSL / macOS : `source venv/bin/activate`  
* Windows (PowerShell) : `.\venv\Scripts\Activate.ps1`  

Installer les dépendances :  
`pip install -r requirements.txt`

### 3. Lancer l'API Externe (Docker)

Assure-toi que le conteneur Docker fourni pour l'exercice tourne bien sur le port **5001** :
* L'API doit être accessible sur : `http://localhost:5001`

### 4. Lancer Ollama avec Qwen

Assure-toi que le service Ollama tourne et que le modèle Qwen est bien disponible :  
`ollama run qwen` (ou la version spécifique utilisée, ex: `qwen2.5`)

### 5. Lancer l'API FastAPI

Dans ton terminal (avec l'environnement virtuel `.venv` activé) :  
`uvicorn app:app --host 0.0.0.0 --port 8000 --reload`

Le serveur sera prêt lorsque tu verras la ligne :  
`INFO: Application startup complete.`

---

## 📡 UTILISATION DE L'API (INTÉGRATION FRONT-END)

L'API expose un point d'entrée HTTP POST pour envoyer des requêtes à l'agent :

* **URL :** `http://localhost:8000/api/chat`
* **Méthode :** `POST`
* **Headers :** `Content-Type: application/json`

### Exemple de corps de requête (Payload) :

`{ "message": "Donne-moi les détails du produit HB-LAP-1001" }`

### Exemple de réponse JSON :

`{ "response": "Détails du produit du catalogue externe :\n- SKU : HB-LAP-1001\n- Nom : Portable Pro...\n" }`
