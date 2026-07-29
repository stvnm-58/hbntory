# routes/

Déclaration des blueprints Flask : chaque fichier associe une URL et une méthode HTTP
à une fonction de [controllers/](../controllers/), en appliquant si besoin un décorateur
d'authentification de [utils/decorators.py](../utils/decorators.py).

- `auth_routes.py` — `/login`, `/register` (public)
- `user_routes.py` — CRUD utilisateurs (`admin_required` sauf lecture d'une fiche)
- `stock_routes.py` — CRUD stock (`jwt_required_custom`)
- `search_routes.py` — recherche produit (monté directement dans [app.py](../app.py))

Les préfixes (`/api/auth`, `/api/users`, ...) sont définis lors de
`app.register_blueprint()` dans [app.py](../app.py), pas ici.

Voir aussi [tests/](tests/) pour les tests associés.
