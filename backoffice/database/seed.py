# Script à lancer manuellement (`python database/seed.py`) pour repartir
# d'une base vierge avec des données de démo (2 branches, 2 users, du stock
# pour tout le catalogue produits de l'API externe)
import sys
import os
import json
import random

# Ajoute la racine du projet au PYTHONPATH pour pouvoir importer app/models
BACKOFFICE_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

REPO_ROOT = os.path.dirname(BACKOFFICE_ROOT)

sys.path.append(BACKOFFICE_ROOT)


from app import create_app

from database.db import db

from models import (
    User,
    Branch,
    Stock
)


# Catalogue produits servi par le container Docker api_extern : on s'en sert
# comme source des SKU à stocker pour ne pas les dupliquer à la main ici
PRODUCTS_FILE = os.path.join(
    REPO_ROOT,
    "api_extern",
    "data",
    "products.json"
)


def load_product_skus():
    # Lit tous les SKU du fichier products.json du container api_extern
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)

    return [product["sku"] for product in data["products"]]



app = create_app()



with app.app_context():


    db.drop_all()

    db.create_all()



    bordeaux = Branch(

        name="Bordeaux",

        location="France"

    )


    paris = Branch(

        name="Paris",

        location="France"

    )


    db.session.add_all(
        [
            bordeaux,
            paris
        ]
    )

    db.session.commit()



    admin = User(

        email="admin@hbntory.com",

        role="admin"

    )


    admin.set_password(
        "admin123"
    )



    employee = User(

        email="employee@hbntory.com",

        role="employee",

        branch_id=bordeaux.id

    )


    employee.set_password(
        "employee123"
    )



    db.session.add_all(
        [
            admin,
            employee
        ]
    )


    db.session.commit()




    # Un stock par produit et par branche, avec une quantité pseudo-aléatoire
    # mais reproductible (seed fixe) pour que les démos restent stables
    rng = random.Random(42)

    skus = load_product_skus()

    stocks = [
        Stock(
            branch_id=branch.id,
            product_sku=sku,
            quantity=rng.randint(0, 80)
        )
        for branch in (bordeaux, paris)
        for sku in skus
    ]



    db.session.add_all(
        stocks
    )


    db.session.commit()



    print("Database seeded")
