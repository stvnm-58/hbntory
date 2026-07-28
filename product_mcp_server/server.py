import os
import requests
from mcp.server.fastmcp import FastMCP

# 1. Initialisation du serveur FastMCP
mcp = FastMCP("HBntory-Product-Catalog")

# URL de l'API externe (Docker sur le port 5001)
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "http://localhost:5001")

@mcp.tool()
def get_external_product(sku: str) -> str:
    """
    Récupère les détails d'un produit (nom, prix, catégorie, marque) 
    depuis le catalogue externe en utilisant son SKU (ex: 'HB-LAP-1001').
    """
    url = f"{EXTERNAL_API_URL}/api/v1/products/{sku}"
    
    try:
        response = requests.get(url, timeout=2.5)
        response.raise_for_status()
        
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
        return "Erreur : L'API externe du catalogue est trop lente à répondre (Timeout)."
    except requests.exceptions.HTTPError as e:
        return f"Erreur : L'API externe a renvoyé une anomalie (Code HTTP {e.response.status_code})."
    except requests.exceptions.RequestException as e:
        return f"Erreur critique : Impossible de joindre l'API externe. Est-elle bien lancée sur le port 5001 ? Détail : {str(e)}"

if __name__ == "__main__":
    # Lancement exclusif en mode stdio pour servir de sous-processus MCP
    mcp.run(transport="stdio")
