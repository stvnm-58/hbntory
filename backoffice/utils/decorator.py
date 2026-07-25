from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)


from flask import jsonify




def jwt_required_custom():

    def decorator(func):

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



            return func(*args, **kwargs)


        return wrapper


    return decorator





def admin_required(func):


    @wraps(func)

    def wrapper(*args, **kwargs):


        verify_jwt_in_request()


        identity = get_jwt_identity()


        if identity["role"] != "admin":

            return jsonify(
                {
                    "error":
                    "Admin only"
                }
            ),403



        return func(*args, **kwargs)


    return wrapper
