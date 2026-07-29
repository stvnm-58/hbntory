# Backoffice hbntory

API Flask de gestion interne pour hbntory : authentification, gestion des utilisateurs,
des succursales (branches), du stock, et recherche de produits croisée avec le stock local.

## Stack

- Flask + Flask-SQLAlchemy (ORM / SQLite par défaut)
- Flask-JWT-Extended (authentification par token)
- pytest (tests)

## Structure du projet

- [controllers/](controllers/) — logique des requêtes HTTP (parsing, codes de statut)
- [database/](database/) — instance SQLAlchemy et script de seed
- [models/](models/) — modèles de données (User, Branch, Stock)
- [routes/](routes/) — déclaration des blueprints Flask et association route → contrôleur
- [services/](services/) — logique métier et accès aux données/API externes
- [utils/](utils/) — décorateurs (auth) et fonctions utilitaires partagées
- `instance/` — base SQLite locale générée au runtime (non versionnée en prod)

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Variables d'environnement (voir [config.py](config.py)), à définir dans un fichier `.env` :

| Variable | Rôle | Défaut |
|---|---|---|
| `DATABASE_URL` | URI de connexion SQLAlchemy | `sqlite:///hbntory.db` |
| `JWT_SECRET_KEY` | Clé de signature des tokens JWT | `dev-secret-key` (dev uniquement) |
| `PRODUCT_API_URL` | URL du microservice produits externe | `http://localhost:5001` |

## Lancer l'application

```bash
python app.py
```

L'app démarre sur `http://localhost:5050` avec `debug=True`.

## Initialiser des données de démo

```bash
python database/seed.py
```

Recrée les tables et insère 2 branches, 1 admin, 1 employé et 2 stocks de démo.
⚠️ Supprime toutes les données existantes.

## Tests

```bash
pytest
```

## Routes principales

| Préfixe | Blueprint | Description |
|---|---|---|
| `/api/auth` | `auth_bp` | Login / inscription |
| `/api/users` | `user_bp` | CRUD utilisateurs (admin) |
| `/api/stocks` | `stock_bp` | CRUD stock (authentifié) |
| `/api/search` | `search_bp` | Recherche produit + stock local |
