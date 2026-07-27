from flask import Blueprint


from controllers.stock_controller import (

    get_stocks,

    get_stock_controller,

    create_stock_controller,

    update_stock_controller,

    delete_stock_controller

)



from utils.decorators import jwt_required_custom



stock_bp = Blueprint(
    "stocks",
    __name__
)




stock_bp.route(
    "/",
    methods=["GET"]
)(
    jwt_required_custom(get_stocks)
)




stock_bp.route(
    "/<int:stock_id>",
    methods=["GET"]
)(
    jwt_required_custom(get_stock_controller)
)




stock_bp.route(
    "/",
    methods=["POST"]
)(
    jwt_required_custom(create_stock_controller)
)




stock_bp.route(
    "/<int:stock_id>",
    methods=["PUT"]
)(
    jwt_required_custom(update_stock_controller)
)




stock_bp.route(
    "/<int:stock_id>",
    methods=["DELETE"]
)(
    jwt_required_custom(delete_stock_controller)
)
