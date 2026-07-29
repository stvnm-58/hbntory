from flask import request, jsonify

from services.search_service import search_products


def search():
    # Recherche produit : délègue à l'API externe puis croise avec le stock local
    query = request.args.get("q", "").strip()

    try:
        results = search_products(query)
        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
