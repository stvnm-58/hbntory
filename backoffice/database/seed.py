from werkzeug.security import generate_password_hash

from app import create_app

from database.db import db
from models.user import User
from models.branch import Branch
from models.stock import Stock


def seed():

    # Vérifie si la base contient déjà des données
    if User.query.first():
        print("Database already initialized")
        return


    # Création des branches

    bordeaux = Branch(
        name="Bordeaux",
        location="Bordeaux"
    )

    paris = Branch(
        name="Paris",
        location="Paris"
    )

    db.session.add_all([
        bordeaux,
        paris
    ])

    db.session.commit()


    # Création des utilisateurs

    admin = User(
        username="admin",
        email="admin@hbntory.com",
        password_hash=generate_password_hash(
            "admin123"
        ),
        role="admin",
        branch_id=None,
        is_deleted=False
    )


    employee = User(
        username="employee",
        email="employee@hbntory.com",
        password_hash=generate_password_hash(
            "employee123"
        ),
        role="employee",
        branch_id=bordeaux.id,
        is_deleted=False
    )


    db.session.add_all([
        admin,
        employee
    ])

    db.session.commit()


    # Création du stock

    stocks = [

        Stock(
            branch_id=bordeaux.id,
            product_sku="HB-LAP-1001",
            quantity=10
        ),

        Stock(
            branch_id=bordeaux.id,
            product_sku="HB-MON-2001",
            quantity=5
        ),

        Stock(
            branch_id=paris.id,
            product_sku="HB-LAP-1001",
            quantity=3
        )
    ]


    db.session.add_all(stocks)

    db.session.commit()


    print("Database initialized successfully")


if __name__ == "__main__":

    app = create_app()

    with app.app_context():
        seed()
