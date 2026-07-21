from werkzeug.security import generate_password_hash

from app import create_app
from database.db import db

from models.user import User
from models.branch import Branch
from models.stock import Stock


def seed_database():

    app = create_app()

    with app.app_context():

        # Nettoyage optionnel
        db.drop_all()
        db.create_all()


        # Création des branches

        bordeaux = Branch(
            name="Bordeaux",
            location="Bordeaux"
        )

        paris = Branch(
            name="Paris",
            location="Paris"
        )


        db.session.add(bordeaux)
        db.session.add(paris)

        db.session.commit()


        # Création admin

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


        db.session.add(admin)


        # Création utilisateur test

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


        db.session.add(employee)

        db.session.commit()


        # Stock de test

        stock1 = Stock(
            branch_id=bordeaux.id,
            product_id=1,
            quantity=20
        )


        stock2 = Stock(
            branch_id=bordeaux.id,
            product_id=2,
            quantity=15
        )


        stock3 = Stock(
            branch_id=paris.id,
            product_id=1,
            quantity=10
        )


        db.session.add_all(
            [
                stock1,
                stock2,
                stock3
            ]
        )


        db.session.commit()


        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()
