# Client Web

Interface publique du projet HBntory : une page permettant à n'importe quel visiteur (anonyme, pas de connexion) de rechercher des produits/du stock ou de poser une question en langage naturel à un assistant.

HTML / CSS / JS simple, sans framework ni dépendance.

## Structure

```
client_web/
├── index.html        # page unique : recherche + bulle de chat flottante
├── css/
│   └── style.css
├── js/
│   ├── app.js          # config partagée + wrapper fetch (API_BASE_URL)
│   ├── search.js        # tableau de résultats (façon Excel)
│   └── chat.js          # bulle déplaçable, panneau de chat, envoi de message
└── assets/
```

## Lancer en local

```bash
cd client_web
python3 -m http.server 8000
```

Puis ouvrir `http://localhost:8000` dans un navigateur.

## État de l'intégration

La recherche (`fetchResults`) et le chat (`askBot`) sont pour l'instant des **stubs** : l'interface fonctionne déjà (onglets, bulle, envoi de message) mais aucune donnée réelle n'est encore récupérée.

Une fois `ai_service` disponible :
1. Renseigner `API_BASE_URL` dans `js/app.js`.
2. Faire appeler `apiFetch(...)` par `fetchResults()` et `askBot()` au lieu de leurs valeurs stub.

Le front ne communique jamais directement avec le serveur MCP — uniquement avec `ai_service`.
