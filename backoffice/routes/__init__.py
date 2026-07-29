# Ré-exporte les blueprints Flask (search_bp est importé directement
# depuis routes.search_routes dans app.py, pas via ce module)
from .auth_routes import auth_bp
from .user_routes import user_bp
from .stock_routes import stock_bp
