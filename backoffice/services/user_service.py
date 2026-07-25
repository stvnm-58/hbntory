from database.db import db
from models.user import User
from werkzeug.security import generate_password_hash


def get_all_users():
    """
    Retourne tous les utilisateurs actifs
    """

    return User.query.filter_by(
        is_deleted=False
    ).all()



def get_user_by_id(user_id):
    """
    Retourne un utilisateur par son ID
    """

    return User.query.filter_by(
        id=user_id,
        is_deleted=False
    ).first()



def create_user(data):
    """
    Crée un nouvel utilisateur
    """

    if not data.get("email") or not data.get("password"):
        return None


    user = User(
        email=data["email"],
        password_hash=generate_password_hash(
            data["password"]
        ),
        role=data.get("role", "employee"),
        branch_id=data.get("branch_id"),
        is_deleted=False
    )


    db.session.add(user)
    db.session.commit()

    return user



def update_user(user_id, data):
    """
    Modifie les informations d'un utilisateur
    """

    user = get_user_by_id(user_id)

    if not user:
        return None


    if "email" in data:
        user.email = data["email"]


    if "password" in data:
        user.password_hash = generate_password_hash(
            data["password"]
        )


    if "role" in data:
        user.role = data["role"]


    if "branch_id" in data:
        user.branch_id = data["branch_id"]


    db.session.commit()

    return user



def delete_user(user_id):
    """
    Suppression logique d'un utilisateur
    (soft delete)
    """

    user = get_user_by_id(user_id)

    if not user:
        return False


    user.is_deleted = True

    db.session.commit()

    return True
