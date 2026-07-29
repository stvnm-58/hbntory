from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    # Compte d'accès au backoffice (admin ou employee, rattaché à une branche)
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="employee")
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.id"), nullable=True)

    # Soft delete : les users supprimés restent en base mais filtrés par user_service
    is_deleted = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        # Hash le mot de passe, jamais stocké en clair
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Vérifie un mot de passe en clair contre le hash stocké
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        # Sérialisation JSON utilisée par les controllers (pas de password_hash exposé)
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "branch_id": self.branch_id
        }
