from flask import Blueprint

from controllers.stock_controller import (
    get_stocks,
    get_stock_controller,
    create_stock_controller,
    update_stock_controller,
    delete_stock_controller
)

from utils.decorators import jwt_required_custom

# Routes CRUD pour le stock, montées sous /api/stocks.
# Toutes exigent un JWT valide (pas de restriction de rôle particulière).
stock_bp = Blueprint("stocks", __name__)

# GET /api/stocks/ : liste tout le stock
stock_bp.route("/", methods=["GET"])(jwt_required_custom(get_stocks))

# GET /api/stocks/<id> : détail d'une ligne de stock
stock_bp.route("/<int:stock_id>", methods=["GET"])(jwt_required_custom(get_stock_controller))

# POST /api/stocks/ : crée une ligne de stock
stock_bp.route("/", methods=["POST"])(jwt_required_custom(create_stock_controller))

# PUT /api/stocks/<id> : met à jour la quantité
stock_bp.route("/<int:stock_id>", methods=["PUT"])(jwt_required_custom(update_stock_controller))

# DELETE /api/stocks/<id> : supprime une ligne de stock
stock_bp.route("/<int:stock_id>", methods=["DELETE"])(jwt_required_custom(delete_stock_controller))
