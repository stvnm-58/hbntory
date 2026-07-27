from flask import request, jsonify

from services.auth_service import login_user, create_user
from flask_jwt_extended import JWTManager


def login():

    data = request.json


    result = login_user(
        data["email"],
        data["password"]
    )


    if not result:

        return jsonify(
            {
                "error": "Invalid credentials"
            }
        ),401


    return jsonify(result),200





def register():

    data = request.json


    user = create_user(

        email=data["email"],

        password=data["password"],

        role=data.get(
            "role",
            "employee"
        ),

        branch_id=data.get(
            "branch_id"
        )

    )

    if not user:

        return jsonify(
            {
                "error":
                "Email already exists"
            }
        ),409



    return jsonify(
        user.to_dict()
    ),201
