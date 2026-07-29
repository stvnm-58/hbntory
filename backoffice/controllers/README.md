# controllers/

Fonctions appelées directement par les routes Flask. Elles s'occupent de :

- lire la requête (`request.json`, `request.args`, params d'URL) ;
- appeler la couche [services/](../services/) pour la logique métier ;
- renvoyer une réponse JSON avec le bon code HTTP.

Aucune requête SQL directe ici (sauf `branch_controller.py`, à harmoniser avec les autres
contrôleurs qui passent tous par `services/`).

## Fichiers

- `auth_controller.py` — login / register
- `branch_controller.py` — CRUD succursales
- `search_controller.py` — recherche produit
- `stock_controller.py` — CRUD stock
- `user_controller.py` — CRUD utilisateurs
