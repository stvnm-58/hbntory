# services/

Logique métier et accès aux données, appelée par [controllers/](../controllers/).
C'est la seule couche censée faire des requêtes SQLAlchemy ou des appels HTTP externes.

- `auth_service.py` — vérification des identifiants, génération de JWT, création de compte
- `user_service.py` — CRUD utilisateurs (lecture filtrée sur `is_deleted=False`)
- `stock_service.py` — CRUD stock
- `product_service.py` — appel au microservice produits externe (`Config.PRODUCT_API_URL`)
- `search_service.py` — combine l'API produits externe et le stock local par SKU
