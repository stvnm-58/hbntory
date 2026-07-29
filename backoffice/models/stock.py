from database.db import db
from datetime import datetime


class Stock(db.Model):
    # Quantité d'un produit (identifié par SKU externe) disponible dans une branche
    __tablename__ = "stocks"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    branch_id = db.Column(
        db.Integer,
        db.ForeignKey("branches.id"),
        nullable=False
    )


    product_sku = db.Column(
        db.String(100),
        nullable=False
    )


    quantity = db.Column(
        db.Integer,
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


    def to_dict(self):
        # Sérialisation JSON utilisée par les controllers
        return {

            "id": self.id,

            "branch_id": self.branch_id,

            "product_sku": self.product_sku,

            "quantity": self.quantity

        }
