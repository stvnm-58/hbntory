# utils/

Fonctions transverses réutilisées dans plusieurs couches.

- `decorators.py` — `jwt_required_custom` (authentification simple) et `admin_required`
  (authentification + rôle admin), à poser sur les fonctions de route
- `helpers.py` — `response()`, format de réponse `{message, data?}` (pas encore utilisé
  par les contrôleurs actuels, qui construisent leur JSON directement)
