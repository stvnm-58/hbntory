# Controllers CRUD pour les utilisateurs, montés sur /api/users. Les routes
# de liste/modification/suppression exigent le rôle admin (voir user_routes.py)
from flask import request, jsonify

from services.user_service import (
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)



def get_users():
    # Liste tous les utilisateurs non supprimés (réservé aux admins)

    users = get_all_users()


    return jsonify(
        [
            user.to_dict()
            for user in users
        ]
    )





def get_user(user_id):
    # Récupère un utilisateur par son id (accessible à tout utilisateur connecté)

    user = get_user_by_id(
        user_id
    )


    if not user:

        return jsonify(
            {
                "error":"User not found"
            }
        ),404



    return jsonify(
        user.to_dict()
    )





def update_user_controller(user_id):
    # Met à jour email/rôle/succursale d'un utilisateur (réservé aux admins)

    user = update_user(
        user_id,
        request.json
    )


    if not user:

        return jsonify(
            {
                "error":
                "User not found"
            }
        ),404



    return jsonify(
        user.to_dict()
    )





def delete_user_controller(user_id):
    # Soft delete d'un utilisateur (réservé aux admins)

    result = delete_user(
        user_id
    )


    if not result:

        return jsonify(
            {
                "error":
                "User not found"
            }
        ),404



    return jsonify(
        {
            "message":
            "User deleted"
        }
    )
