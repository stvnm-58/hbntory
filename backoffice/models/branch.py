from database.db import db


class Branch(db.Model):
    # Succursale physique (magasin/entrepôt) : possède des utilisateurs et du stock
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
        db.String(200),
        nullable=False
    )


    users = db.relationship(
        "User",
        backref="branch",
        lazy=True
    )


    stocks = db.relationship(
        "Stock",
        backref="branch",
        lazy=True
    )


    def to_dict(self):
        # Sérialisation JSON utilisée par les controllers
        return {

            "id": self.id,

            "name": self.name,

            "location": self.location

        }
