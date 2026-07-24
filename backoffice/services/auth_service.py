from models.user import User
from database.db import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token


def authenticate_user(email, password):
    """
    Vérifie les identifiants d'un utilisateur
    """

    user = User.query.filter_by(
        email=email,
        is_deleted=False
    ).first()

    if not user:
        return None

    if not check_password_hash(user.password_hash, password):
        return None

    return user



def generate_token(user):
    """
    Génère un JWT
    """

    token = create_access_token(
        identity={
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    )

    return token



def login(email, password):
    """
    Fonction complète de connexion
    """

    user = authenticate_user(email, password)

    if not user:
        return None

    token = generate_token(user)

    return {
        "user": user,
        "token": token
    }