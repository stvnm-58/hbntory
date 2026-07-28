import requests

from models.stock import Stock


PRODUCT_API_URL = "http://localhost:5001/api/v1/products/search"


def search_products(query):

    # Appel API externe produits

    response = requests.get(
        PRODUCT_API_URL,
        params={
            "q": query,
            "limit": 100
        },
        timeout=5
    )


    response.raise_for_status()


    data = response.json()


    products = data.get(
        "results",
        []
    )


    results = []


    for product in products:

        sku = product.get("sku")


        # Recherche du stock local

        stocks = Stock.query.filter_by(
            product_sku=sku
        ).all()



        if stocks:

            for stock in stocks:

                results.append({

                    "sku": sku,

                    "name": product.get(
                        "name"
                    ),

                    "category": product.get(
                        "category"
                    ),

                    "unit_price": product.get(
                        "unit_price"
                    ),

                    "branch_id": stock.branch_id,

                    "branch_name": (
                        stock.branch.name
                        if stock.branch
                        else None
                    ),

                    "quantity": stock.quantity

                })


        else:

            # Produit existe mais pas de stock local

            results.append({

                "sku": sku,

                "name": product.get(
                    "name"
                ),

                "category": product.get(
                    "category"
                ),

                "unit_price": product.get(
                    "unit_price"
                ),

                "branch_id": None,

                "branch_name": None,

                "quantity": 0

            })


    return results
