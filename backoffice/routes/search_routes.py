# Route de recherche produits, montée sous /api/search. Publique (pas de
# jwt_required) : utilisée par le catalogue visiteur ET par le backoffice.
from flask import Blueprint

from controllers.search_controller import search


search_bp = Blueprint(
    "search",
    __name__
)


# strict_slashes=False : /api/search et /api/search/ répondent tous les deux
search_bp.route(
    "/",
    methods=["GET"],
    strict_slashes=False
)(search)
