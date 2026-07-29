import os
import requests
from mcp.server.fastmcp import FastMCP

# Initialisation du serveur FastMCP pour le catalogue produit
mcp = FastMCP("HBntory-Product-Catalog")

# URL de l'API externe (lecture depuis variable d'environnement avec fallback vers http://localhost:5001)
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "http://localhost:5001")

@mcp.tool()
def get_external_product(sku: str) -> str:
    """
    Récupère les détails d'un produit (nom, prix, catégorie, marque) 
    depuis le catalogue externe en utilisant son SKU (ex: 'HB-LAP-1001').

    Args:
        sku (str): L'identifiant unique (Stock Keeping Unit) du produit recherché.

    Returns:
        str: Une chaîne de caractères formatée contenant les informations du produit 
             en cas de succès, ou un message d'erreur expliquant le problème en cas d'échec.
    """
    url = f"{EXTERNAL_API_URL}/api/v1/products/{sku}"
    
    try:
        # Envoi d'une requête HTTP GET vers l'API externe avec un délai d'expiration fixé à 2.5 secondes
        response = requests.get(url, timeout=2.5)
        
        # Déclenche une exception HTTPError si le statut HTTP renvoyé indique une erreur (ex: 404, 500)
        response.raise_for_status()
        
        # Extraction du corps de la réponse formaté en JSON
        product_data = response.json()
        
        return (
            f"Détails du produit du catalogue externe :\n"
            f"- SKU : {product_data.get('sku')}\n"
            f"- Nom : {product_data.get('name')}\n"
            f"- Marque : {product_data.get('brand')}\n"
            f"- Catégorie : {product_data.get('category')}\n"
            f"- Prix de base : {product_data.get('unit_price')} {product_data.get('currency')}\n"
            f"- Statut catalogue : {'Discontinué' if product_data.get('discontinued') else 'Disponible'}"
        )
        
    except requests.exceptions.Timeout:
        # EXCEPT Timeout :
        # Intercepte le cas où l'API externe met plus de 2.5s à répondre.
        # RETURN (Erreur Timeout) : Renvoie un message d'erreur explicite sans faire planter le serveur.
        return "Erreur : L'API externe du catalogue est trop lente à répondre (Timeout)."

    except requests.exceptions.HTTPError as e:
        # EXCEPT HTTPError :
        # Intercepte les réponses d'erreur HTTP renvoyées par le serveur distants (ex: 404 Not Found, 500 Internal Error).
        # RETURN (Erreur HTTP) : Renvoie le code de statut HTTP exact renvoyé par l'API pour diagnostic.
        return f"Erreur : L'API externe a renvoyé une anomalie (Code HTTP {e.response.status_code})."

    except requests.exceptions.RequestException as e:
        # EXCEPT RequestException :
        # Intercepte toutes les autres erreurs réseau sous-jacentes (ex: serveur indisponible, port fermé, échec DNS).
        # RETURN (Erreur Réseau) : Renvoie le détail complet de l'exception pour identifier le problème de connexion.
        return f"Erreur critique : Impossible de joindre l'API externe (Port 5001). Détail : {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")