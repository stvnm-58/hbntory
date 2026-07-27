from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

from database.db import db
from models.user import User

def login():
    data = request.get_json()
    
    if not data :
        return jsonify({"error": "Missing data "}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email or password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Invalid credential"}), 401
    
    if user.id_deleted:
        return jsonify({"error": "User account is deleted"}), 403
    
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credential"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

    return jsonify({
        "Message": "Login successful",
        "access_token": access_token
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
        user = User.query.get(user_id)
        
        if not user or user.id_deleted:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "branch_id": user.branch_id
        }), 200
