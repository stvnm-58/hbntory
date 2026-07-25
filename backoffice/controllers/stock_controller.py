from flask import request, jsonify


from services.stock_service import (
    get_all_stocks,
    get_stock,
    create_stock,
    update_stock,
    delete_stock
)




def get_stocks():

    stocks = get_all_stocks()


    return jsonify(
        [
            stock.to_dict()
            for stock in stocks
        ]
    )





def get_stock_controller(stock_id):


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


    stock = create_stock(
        request.json
    )


    return jsonify(
        stock.to_dict()
    ),201





def update_stock_controller(stock_id):


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
