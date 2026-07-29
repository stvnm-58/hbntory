# Routes d'authentification, montées sous /api/auth. Publiques : pas de
# jwt_required ici, forcément (login/register précèdent l'obtention du JWT).
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


# POST /api/auth/login : vérifie les identifiants, renvoie un JWT
auth_bp.route(
    "/login",
    methods=["POST"]
)(login)


# POST /api/auth/register : crée un nouvel utilisateur
auth_bp.route(
    "/register",
    methods=["POST"]
)(register)
