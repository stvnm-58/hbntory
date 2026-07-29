# database/

Configuration de l'accès aux données.

- `db.py` — instance unique `SQLAlchemy()`, liée à l'app dans [app.py](../app.py)
- `seed.py` — script autonome pour repartir d'une base vierge avec des données de démo
  (`python database/seed.py`, à lancer depuis la racine `backoffice/`)

Les tables sont créées automatiquement au démarrage de l'app via `db.create_all()`
(voir [app.py](../app.py)) ; ce dossier ne contient donc pas de migrations.
