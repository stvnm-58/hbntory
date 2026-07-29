# Logique métier CRUD pour le stock (accès direct aux modèles SQLAlchemy)
from models.stock import Stock
from database.db import db


def get_all_stocks():
    # Renvoie toutes les lignes de stock, toutes succursales confondues
    return Stock.query.all()


def get_stock(stock_id):
    # Renvoie une ligne de stock par id, ou None si absente
    return Stock.query.get(stock_id)


def create_stock(data):
    # branch_id et product_sku sont requis, quantity vaut 0 par défaut
    stock = Stock(
        branch_id=data["branch_id"],
        product_sku=data["product_sku"],
        quantity=data.get("quantity", 0)
    )

    db.session.add(stock)
    db.session.commit()

    return stock


def update_stock(stock_id, data):
    # Met à jour la quantité d'une ligne de stock existante
    stock = get_stock(stock_id)

    if not stock:
        return None

    if "quantity" in data:
        stock.quantity = data["quantity"]

    db.session.commit()

    return stock


def delete_stock(stock_id):
    # Supprime définitivement une ligne de stock
    stock = get_stock(stock_id)

    if not stock:
        return False

    db.session.delete(stock)
    db.session.commit()

    return True
