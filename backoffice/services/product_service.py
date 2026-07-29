# Client HTTP vers l'API produits externe (container Docker api_extern)
import requests

from config import Config



def get_product(product_sku):
    # Récupère un produit du catalogue externe par son SKU, ou None si absent/erreur

    url = (
        f"{Config.PRODUCT_API_URL}"
        f"/products/{product_sku}"
    )


    response = requests.get(url)


    if response.status_code != 200:

        return None



    return response.json()
