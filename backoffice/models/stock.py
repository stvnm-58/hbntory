from datetime import datetime

from sqlalchemy import CheckConstraint

from database.db import db


class Stock(db.Model):

    __tablename__ = "stock"


    __table_args__ = (
        CheckConstraint(
            "quantity >= 0",
            name="check_quantity_positive"
        ),
    )


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    branch_id = db.Column(
        db.Integer,
        db.ForeignKey("branches.id"),
        nullable=False
    )


    # Référence vers le Product API
    # Exemple : HB-LAP-1001
    product_sku = db.Column(
        db.String(100),
        nullable=False
    )


    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
