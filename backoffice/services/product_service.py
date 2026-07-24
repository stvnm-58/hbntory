import requests
from config import Config



def get_product(product_sku):

    url = f"{Config.PRODUCT_API_URL}/{product_sku}"


    response = requests.get(url)


    if response.status_code != 200:
        return None


    return response.json()
