# Logique métier CRUD pour les utilisateurs (exclut toujours les soft-deleted)
from models.user import User
from database.db import db



def get_all_users():
    # Renvoie tous les utilisateurs actifs (non soft-deleted)
    return User.query.filter_by(
        is_deleted=False
    ).all()



def get_user_by_id(user_id):
    # Renvoie un utilisateur actif par id, ou None si absent/supprimé
    return User.query.filter_by(
        id=user_id,
        is_deleted=False
    ).first()



def update_user(user_id, data):
    # Met à jour email/rôle/succursale d'un utilisateur existant
    user = get_user_by_id(user_id)


    if not user:
        return None


    if "email" in data:
        user.email = data["email"]


    if "role" in data:
        user.role = data["role"]


    if "branch_id" in data:
        user.branch_id = data["branch_id"]


    db.session.commit()


    return user




def delete_user(user_id):
    # Marque l'utilisateur comme supprimé (soft delete)
    user = get_user_by_id(user_id)


    if not user:
        return False


    # Soft delete demandé dans le cahier des charges

    user.is_deleted = True


    db.session.commit()


    return True
