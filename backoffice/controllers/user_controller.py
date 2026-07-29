# CRUD des utilisateurs, monté sur /api/users (liste/modif/suppression réservées aux admins)
from flask import request, jsonify

from services.user_service import (
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)


def get_users():
    # Liste tous les utilisateurs
    users = get_all_users()

    return jsonify([user.to_dict() for user in users])


def get_user(user_id):
    # Récupère un utilisateur par id
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict())


def update_user_controller(user_id):
    # Met à jour email/rôle/succursale d'un utilisateur
    user = update_user(user_id, request.json)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict())


def delete_user_controller(user_id):
    # Supprime (soft delete) un utilisateur
    result = delete_user(user_id)

    if not result:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted"})
