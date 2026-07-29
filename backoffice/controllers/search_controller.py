# Controller de recherche produits, monté sur /api/search (accessible sans
# authentification : utilisé par le catalogue public et par le backoffice)
from flask import request, jsonify

from services.search_service import search_products


def search():
    query = request.args.get("q", "").strip()

    try:
        results = search_products(query)
        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
