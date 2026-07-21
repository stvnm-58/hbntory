# 🔌 Product MCP Server

Serveur MCP permettant d'interconnecter l'IA à notre API d'inventaire Docker.

---

## 🚀 Guide de lancement rapide

Il faut **2 terminaux ouverts** en même temps.

### 1 Terminal 1 : Lancer l'API Docker

# Aller dans le dossier de l'API Docker
docker compose up --build





### 2 Terminal 2 : venv

# 1. Aller dans le dossier
cd product_mcp_server

# 2. Créer le venv local
python3 -m venv venv

# 3. Activer le venv
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt



### 3 Tester le serveur avec l'interface MCP Inspector

Une fois le `venv` prêt et l'API Docker lancée :

1. Lance l'Inspecteur dans ton terminal :
   ```bash
   npx @modelcontextprotocol/inspector