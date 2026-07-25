from app import create_app

from database.db import db

from models import (
    User,
    Branch,
    Stock
)



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




    stocks = [

        Stock(

            branch_id=bordeaux.id,

            product_sku="SKU001",

            quantity=50

        ),


        Stock(

            branch_id=paris.id,

            product_sku="SKU002",

            quantity=20

        )

    ]



    db.session.add_all(
        stocks
    )


    db.session.commit()



    print("Database seeded")
