from flask import request, jsonify
from services.stock_service import (
    get_all_stocks,
    get_stock_by_id,
    create_stock,
    update_stock,
    delete_stock
)

def get_stocks():
    stocks = get_all_stocks()
    return jsonify(stocks), 200

def get_stock(stock_id):
    stock = get_stock_by_id(stock_id)
    if not stock:
        return jsonify({"error": "Stock not found"}), 404
    return jsonify(stock), 200

def create_stock():
    data = request.get_json()
    stock = create_stock(data)
    return jsonify(stock), 201

def update_stock(stock_id):
    data = request.get_json()
    stock = update_stock(stock_id, data)
    if not stock:
        return jsonify({"error": "Stock not found"}), 404
    return jsonify(stock), 200

def delete_stock(stock_id):
    stock = delete_stock(stock_id)
    if not stock:
        return jsonify({"error": "Stock not found"}), 404
    return jsonify({"message": "Stock deleted"}), 200
