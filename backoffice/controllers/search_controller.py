from flask import request, jsonify

from services.search_service import search_products


def search():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"error": "Le paramètre 'q' est obligatoire."}), 400

    try:
        results = search_products(query)
        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
