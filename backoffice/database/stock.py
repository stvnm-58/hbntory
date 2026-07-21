from database.db import db
from datetime import datetime


class Stock(db.Model):

    __tablename__ = "stock"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    branch_id = db.Column(
        db.Integer,
        db.ForeignKey("branches.id"),
        nullable=False
    )

    # Identifiant provenant du Product API
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