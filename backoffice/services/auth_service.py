# Logique métier pour la connexion et la création de comptes utilisateurs
from models.user import User
from database.db import db

from flask_jwt_extended import create_access_token


def login_user(email, password):
    # Retourne None si l'email est inconnu, supprimé, ou le mot de passe invalide
    user = User.query.filter_by(email=email, is_deleted=False).first()

    if not user:
        return None

    if not user.check_password(password):
        return None

    # Le rôle est embarqué dans le token pour être lu par admin_required sans requête DB
    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return {"token": token, "user": user.to_dict()}


def create_user(email, password, role="employee", branch_id=None):
    # Unicité de l'email : renvoie None si un compte existe déjà (même soft-deleted)
    existing = User.query.filter_by(email=email).first()

    if existing:
        return None

    user = User(email=email, role=role, branch_id=branch_id)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user
