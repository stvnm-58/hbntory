# Controllers CRUD pour le stock (quantité d'un produit dans une succursale),
# montés sur /api/stocks par routes/stock_routes.py
from flask import request, jsonify


from services.stock_service import (
    get_all_stocks,
    get_stock,
    create_stock,
    update_stock,
    delete_stock
)




def get_stocks():
    # Liste toutes les lignes de stock, toutes succursales confondues
    stocks = get_all_stocks()


    return jsonify(
        [
            stock.to_dict()
            for stock in stocks
        ]
    )





def get_stock_controller(stock_id):
    # Récupère une ligne de stock par son id

    stock = get_stock(
        stock_id
    )


    if not stock:

        return jsonify(
            {
                "error":
                "Stock not found"
            }
        ),404



    return jsonify(
        stock.to_dict()
    )





def create_stock_controller():
    # Crée une ligne de stock (branch_id + product_sku, quantity optionnelle)

    stock = create_stock(
        request.json
    )


    return jsonify(
        stock.to_dict()
    ),201





def update_stock_controller(stock_id):
    # Met à jour la quantité d'une ligne de stock existante

    stock = update_stock(
        stock_id,
        request.json
    )


    if not stock:

        return jsonify(
            {
                "error":
                "Stock not found"
            }
        ),404



    return jsonify(
        stock.to_dict()
    )





def delete_stock_controller(stock_id):
    # Supprime une ligne de stock

    result = delete_stock(
        stock_id
    )


    if not result:

        return jsonify(
            {
                "error":
                "Stock not found"
            }
        ),404



    return jsonify(
        {
            "message":
            "Stock deleted"
        }
    )
