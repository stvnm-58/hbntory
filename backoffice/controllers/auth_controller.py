from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.auth_service import (
    login_user,
    get_user_from_token
)


def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Missing data"
        }), 400


    email = data.get("email")
    password = data.get("password")


    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400


    result = login_user(
        email,
        password
    )


    if not result:
        return jsonify({
            "error": "Invalid credentials"
        }), 401


    user = result["user"]


    return jsonify({
        "message": "Login successful",
        "access_token": result["access_token"],
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "branch_id": user.branch_id
        }
    }), 200



@jwt_required()
def me():

    user_id = get_jwt_identity()


    user = get_user_from_token(user_id)


    if not user:
        return jsonify({
            "error": "User not found"
        }), 404


    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "branch_id": user.branch_id
    }), 200
