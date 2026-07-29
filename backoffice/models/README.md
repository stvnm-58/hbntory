# models/

Modèles SQLAlchemy (`db.Model`).

- `user.py` — comptes d'accès (`admin` / `employee`), mot de passe hashé,
  suppression logique via `is_deleted`
- `branch.py` — succursales, relation 1-N vers `User` et `Stock`
- `stock.py` — quantité d'un produit (`product_sku`, référence externe) par succursale

Chaque modèle expose une méthode `to_dict()` utilisée par les contrôleurs pour la
sérialisation JSON.
