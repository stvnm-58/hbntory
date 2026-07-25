from functools import wraps

from flask import jsonify

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity
)



def jwt_required_custom(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:

            verify_jwt_in_request()

        except Exception:

            return jsonify(
                {
                    "error":
                    "Authentication required"
                }
            ), 401


        return func(*args, **kwargs)


    return wrapper





def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:

            verify_jwt_in_request()

        except Exception:

            return jsonify(
                {
                    "error":
                    "Authentication required"
                }
            ),401



        user = get_jwt_identity()


        if user["role"] != "admin":

            return jsonify(
                {
                    "error":
                    "Admin access required"
                }
            ),403



        return func(*args, **kwargs)


    return wrapper
