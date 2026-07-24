from database.db import db
from models.stock import Stock



def get_all_stock():

    return Stock.query.all()



def get_stock_by_branch(branch_id):

    return Stock.query.filter_by(
        branch_id=branch_id
    ).all()



def get_stock_item(stock_id):

    return Stock.query.get(stock_id)



def create_stock(data):

    stock = Stock(
        branch_id=data["branch_id"],
        product_sku=data["product_sku"],
        quantity=data["quantity"]
    )


    db.session.add(stock)
    db.session.commit()

    return stock



def update_stock(stock_id, quantity):

    stock = get_stock_item(stock_id)


    if not stock:
        return None


    stock.quantity = quantity

    db.session.commit()

    return stock



def add_quantity(stock_id, amount):

    stock = get_stock_item(stock_id)


    if not stock:
        return None


    stock.quantity += amount

    db.session.commit()

    return stock



def remove_quantity(stock_id, amount):

    stock = get_stock_item(stock_id)


    if not stock:
        return None


    if stock.quantity < amount:
        return False


    stock.quantity -= amount

    db.session.commit()

    return stock
