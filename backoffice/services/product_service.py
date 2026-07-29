import requests

from config import Config



def get_product(product_sku):
    # Récupère les infos d'un produit auprès du microservice produits externe
    url = (
        f"{Config.PRODUCT_API_URL}"
        f"/products/{product_sku}"
    )


    response = requests.get(url)


    if response.status_code != 200:

        return None



    return response.json()
