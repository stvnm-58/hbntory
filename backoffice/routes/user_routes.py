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



user_bp = Blueprint(
    "users",
    __name__
)


# Liste, modification et suppression réservées aux admins ; la fiche d'un
# utilisateur est accessible à tout utilisateur authentifié
user_bp.route(
    "/",
    methods=["GET"]
)(
    admin_required(get_users)
)



user_bp.route(
    "/<int:user_id>",
    methods=["GET"]
)(
    jwt_required_custom(get_user)
)



user_bp.route(
    "/<int:user_id>",
    methods=["PUT"]
)(
    admin_required(update_user_controller)
)



user_bp.route(
    "/<int:user_id>",
    methods=["DELETE"]
)(
    admin_required(delete_user_controller)
)
