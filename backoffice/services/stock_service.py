from database.db import db
from models.stock import Stock


def get_all_stock():
    """
    Retourne tout le stock
    """

    return Stock.query.all()



def get_stock_by_id(stock_id):
    """
    Retourne un stock par son ID
    """

    return Stock.query.filter_by(
        id=stock_id
    ).first()



def get_stock_by_branch(branch_id):
    """
    Retourne le stock d'une branche
    """

    return Stock.query.filter_by(
        branch_id=branch_id
    ).all()



def create_stock(data):
    """
    Ajoute un produit au stock
    """

    stock = Stock(
        branch_id=data["branch_id"],
        product_sku=data["product_sku"],
        quantity=data.get("quantity", 0)
    )


    db.session.add(stock)
    db.session.commit()

    return stock



def update_stock(stock_id, data):
    """
    Modifie une quantité de stock
    """

    stock = get_stock_by_id(stock_id)

    if not stock:
        return None


    if "quantity" in data:
        stock.quantity = data["quantity"]


    db.session.commit()

    return stock



def delete_stock(stock_id):
    """
    Supprime un stock
    """

    stock = get_stock_by_id(stock_id)

    if not stock:
        return False


    db.session.delete(stock)
    db.session.commit()

    return True
