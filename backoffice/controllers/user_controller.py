from flask import request, jsonify

from services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user as create_user_service,
    update_user as update_user_service,
    delete_user as delete_user_service
)


def user_to_dict(user):
    """
    Transforme un objet User SQLAlchemy en JSON
    """

    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "branch_id": user.branch_id,
        "is_deleted": user.is_deleted
    }



def get_users():
    """
    Récupérer tous les utilisateurs
    """

    users = get_all_users()

    return jsonify([
        user_to_dict(user)
        for user in users
    ]), 200



def get_user(user_id):
    """
    Récupérer un utilisateur par son ID
    """

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404


    return jsonify(
        user_to_dict(user)
    ), 200



def create_user():
    """
    Créer un utilisateur
    """

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Missing data"
        }), 400


    user = create_user_service(data)

    if not user:
        return jsonify({
            "error": "Email and password are required"
        }), 400


    return jsonify(
        user_to_dict(user)
    ), 201



def update_user(user_id):
    """
    Modifier un utilisateur
    """

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Missing data"
        }), 400


    user = update_user_service(
        user_id,
        data
    )


    if not user:
        return jsonify({
            "error": "User not found"
        }), 404


    return jsonify(
        user_to_dict(user)
    ), 200



def delete_user(user_id):
    """
    Suppression logique d'un utilisateur
    """

    deleted = delete_user_service(user_id)


    if not deleted:
        return jsonify({
            "error": "User not found"
        }), 404


    return jsonify({
        "message": "User deleted successfully"
    }), 200
