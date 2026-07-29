from flask import Blueprint

from controllers.user_controller import (
    get_users,
    get_user,
    update_user_controller,
    delete_user_controller
)

from utils.decorators import (
    jwt_required_custom,
    admin_required
)

# Routes CRUD pour les utilisateurs, montées sous /api/users.
# Liste/modification/suppression réservées aux admins ; le détail est
# accessible à tout utilisateur connecté.
user_bp = Blueprint("users", __name__)

# GET /api/users/ : liste tous les utilisateurs (admin uniquement)
user_bp.route("/", methods=["GET"])(admin_required(get_users))

# GET /api/users/<id> : détail d'un utilisateur (tout utilisateur connecté)
user_bp.route("/<int:user_id>", methods=["GET"])(jwt_required_custom(get_user))

# PUT /api/users/<id> : met à jour un utilisateur (admin uniquement)
user_bp.route("/<int:user_id>", methods=["PUT"])(admin_required(update_user_controller))

# DELETE /api/users/<id> : soft delete d'un utilisateur (admin uniquement)
user_bp.route("/<int:user_id>", methods=["DELETE"])(admin_required(delete_user_controller))
