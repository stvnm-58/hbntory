# Client Web

Interface publique du projet HBntory : une page permettant à n'importe quel visiteur (anonyme, pas de connexion) de rechercher des produits/du stock ou de poser une question en langage naturel à un assistant IA.

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

## Exemples de questions (chat)

- **Détails produit** : « Donne-moi les détails du produit XX. »
- **Disponibilité par succursale** : « Quelle succursale a le stock du produit X ? »
- **Produits d'une succursale** : « Quels produits puis-je trouver dans la succursale Y ? »
- **Liste d'achats** : « Si je veux acheter 3 unités de X, 2 unités de Y et 4 unités de Z, quelle(s) succursale(s) devrais-je visiter ? »

## État de l'intégration

Le chat (`askBot` dans `js/chat.js`) appelle déjà `fetch(...)` vers `ai_service` (feedback de chargement + message d'erreur si le service ne répond pas). Il ne reste qu'à renseigner `AI_SERVICE_URL` une fois `ai_service` disponible.

La recherche (`fetchResults` dans `js/search.js`) est encore un stub à brancher de la même façon.

Le front ne communique jamais directement avec le serveur MCP — uniquement avec `ai_service`.
