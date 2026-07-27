from flask import request, jsonify
from services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)

def get_users():
    users = get_all_users()
    return jsonify(users), 200

def get_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

def add_user():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Missing data"}), 400
    user = create_user(data)
    return jsonify(user), 201

def edit_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing data"}), 400

    user = update_user(user_id, data)

    if user is None:
        return jsonify({"error": "User not found"}), 404


    return jsonify(user), 200

def remove_user(user_id):
    deleted = delete_user(user_id)
    
    if not deleted:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted"}), 200
