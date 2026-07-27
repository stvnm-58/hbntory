<<<<<<< HEAD
import os
import requests
from mcp.server.fastmcp import FastMCP

# 1. Initialisation du serveur MCP avec le framework FastMCP
mcp = FastMCP("HBntory-Product-Catalog")

# URL de l'API externe fournie par le conteneur Docker (port 5001)
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "http://localhost:5001")

@mcp.tool()
def get_external_product(sku: str) -> str:
    """
    Récupère les détails d'un produit (nom, prix, catégorie, marque) 
    depuis le catalogue externe de l'exercice en utilisant son SKU (ex: 'HB-LAP-1001').
    """
    url = f"{EXTERNAL_API_URL}/api/v1/products/{sku}"
    
    try:
        # Timeout de 2.5 secondes max au cas où il y a une simulation de délai (simulate_delay_ms)
        response = requests.get(url, timeout=2.5)
        
        # Si le prof force une erreur (force_error=true), raise_for_status intercepte le crash
        response.raise_for_status()
        
        product_data = response.json()
        
        # Formatage propre de la réponse textuelle que le LLM va lire
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
        return "Erreur : L'API externe du catalogue est trop lente à répondre (Timeout de sécurité MCP déclenché)."
    except requests.exceptions.HTTPError as e:
        return f"Erreur : L'API externe a renvoyé une anomalie (Code HTTP {e.response.status_code})."
    except requests.exceptions.RequestException as e:
        return f"Erreur critique : Impossible de joindre l'API externe. Est-elle bien lancée sur le port 5001 ? Détail : {str(e)}"

if __name__ == "__main__":
    # Lancement obligatoire en mode stdio pour la communication avec l'IA
=======
from mcp.server.fastmcp import FastMCP
import httpx

# Création du serveur MCP
mcp = FastMCP("ProductServer")

@mcp.tool()
async def get_external_product(product_ref: str) -> dict:
    """Récupère les informations d'un produit depuis l'API externe."""
    async with httpx.AsyncClient() as client:
        # URL mise à jour avec le port 5001 et la route /api/v1/products/
        response = await client.get(f"http://localhost:5001/api/v1/products/{product_ref}")
        return response.json()

if __name__ == "__main__":
>>>>>>> 7d4f579 (fix de agent.py pour passer sur ollama qwen et fix server.py. Création API : app.py)
    mcp.run(transport="stdio")