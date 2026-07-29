# Combine le catalogue produits externe (Docker) et le stock local par SKU :
# c'est ce service qui alimente le catalogue visiteur et la recherche backoffice
import requests

from models.stock import Stock

# NOTE : URL en dur plutôt que Config.PRODUCT_API_URL (utilisé par product_service)
PRODUCT_API_URL = "http://localhost:5001/api/v1/products/search"


def search_products(query):
    # Combine les résultats de l'API produits externe avec le stock local par SKU
    response = requests.get(
        PRODUCT_API_URL,
        params={"q": query, "limit": 100},
        timeout=5
    )
    response.raise_for_status()

    data = response.json()
    products = data.get("results", [])

    results = []

    for product in products:
        sku = product.get("sku")

        # Recherche du stock local pour ce SKU (peut être présent dans plusieurs branches)
        stocks = Stock.query.filter_by(product_sku=sku).all()

        if stocks:
            for stock in stocks:
                results.append({
                    "sku": sku,
                    "name": product.get("name"),
                    "category": product.get("category"),
                    "unit_price": product.get("unit_price"),
                    "branch_id": stock.branch_id,
                    "branch_name": stock.branch.name if stock.branch else None,
                    "quantity": stock.quantity
                })
        else:
            # Produit existe côté API externe mais pas de stock local
            results.append({
                "sku": sku,
                "name": product.get("name"),
                "category": product.get("category"),
                "unit_price": product.get("unit_price"),
                "branch_id": None,
                "branch_name": None,
                "quantity": 0
            })

    return results
