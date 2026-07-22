from datetime import datetime

from database.db import db


class Branch(db.Model):

    __tablename__ = "branches"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(255),
        nullable=False
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


    # Relation avec les utilisateurs
    users = db.relationship(
        "User",
        backref="branch",
        lazy=True
    )


    # Relation avec le stock
    stocks = db.relationship(
        "Stock",
        backref="branch",
        lazy=True
    )
