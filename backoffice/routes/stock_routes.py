from flask import Blueprint

from controllers.stock_controller import (
    get_stocks,
    get_stock,
    get_branch_stock,
    create_stock,
    update_stock,
    delete_stock
)


stock_bp = Blueprint("stock", __name__)


stock_bp.route(
    "/",
    methods=["GET"]
)(get_stocks)


stock_bp.route(
    "/<int:stock_id>",
    methods=["GET"]
)(get_stock)


stock_bp.route(
    "/branch/<int:branch_id>",
    methods=["GET"]
)(get_branch_stock)


stock_bp.route(
    "/",
    methods=["POST"]
)(create_stock)


stock_bp.route(
    "/<int:stock_id>",
    methods=["PUT"]
)(update_stock)


stock_bp.route(
    "/<int:stock_id>",
    methods=["DELETE"]
)(delete_stock)
