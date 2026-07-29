from flask import Blueprint

from controllers.auth_controller import (
    login,
    register
)


auth_bp = Blueprint(
    "auth",
    __name__
)

# Routes publiques, aucun JWT requis pour se connecter ou s'inscrire



auth_bp.route(
    "/login",
    methods=["POST"]
)(login)



auth_bp.route(
    "/register",
    methods=["POST"]
)(register)
