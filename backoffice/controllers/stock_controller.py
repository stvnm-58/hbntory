from flask import request, jsonify

from services.stock_service import (
    get_all_stock,
    get_stock_by_id,
    get_stock_by_branch,
    create_stock as create_stock_service,
    update_stock as update_stock_service,
    delete_stock as delete_stock_service
)



def stock_to_dict(stock):

    return {
        "id": stock.id,
        "branch_id": stock.branch_id,
        "product_sku": stock.product_sku,
        "quantity": stock.quantity,
        "created_at": stock.created_at,
        "updated_at": stock.updated_at
    }



def get_stocks():

    stocks = get_all_stock()

    return jsonify([
        stock_to_dict(stock)
        for stock in stocks
    ]), 200



def get_stock(stock_id):

    stock = get_stock_by_id(stock_id)


    if not stock:
        return jsonify({
            "error": "Stock not found"
        }), 404


    return jsonify(
        stock_to_dict(stock)
    ), 200



def get_branch_stock(branch_id):

    stocks = get_stock_by_branch(branch_id)

    return jsonify([
        stock_to_dict(stock)
        for stock in stocks
    ]), 200



def create_stock():

    data = request.get_json()


    if not data:
        return jsonify({
            "error": "Missing data"
        }), 400


    stock = create_stock_service(data)


    return jsonify(
        stock_to_dict(stock)
    ), 201



def update_stock(stock_id):

    data = request.get_json()


    if not data:
        return jsonify({
            "error": "Missing data"
        }), 400


    stock = update_stock_service(
        stock_id,
        data
    )


    if not stock:
        return jsonify({
            "error": "Stock not found"
        }), 404


    return jsonify(
        stock_to_dict(stock)
    ), 200



def delete_stock(stock_id):

    deleted = delete_stock_service(stock_id)


    if not deleted:
        return jsonify({
            "error": "Stock not found"
        }), 404


    return jsonify({
        "message": "Stock deleted"
    }), 200
