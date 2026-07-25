from models.stock import Stock
from database.db import db



def get_all_stocks():

    return Stock.query.all()




def get_stock(stock_id):

    return Stock.query.get(stock_id)




def create_stock(data):


    stock = Stock(

        branch_id=data["branch_id"],

        product_sku=data["product_sku"],

        quantity=data.get(
            "quantity",
            0
        )

    )


    db.session.add(stock)

    db.session.commit()


    return stock




def update_stock(stock_id, data):


    stock = get_stock(stock_id)


    if not stock:
        return None



    if "quantity" in data:

        stock.quantity = data["quantity"]



    db.session.commit()


    return stock




def delete_stock(stock_id):


    stock = get_stock(stock_id)


    if not stock:
        return False



    db.session.delete(stock)

    db.session.commit()


    return True
