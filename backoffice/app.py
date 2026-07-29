# Point d'entrée de l'API backoffice : assemble la config, la base et les
# blueprints (auth, users, stocks, search) en une application Flask.
from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config
from database.db import db

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.stock_routes import stock_bp
from routes.search_routes import search_bp


def create_app():
    # Factory Flask : crée et configure une nouvelle instance de l'app
    # (utilisé aussi bien par app.run() que par les tests / le seed).

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)


    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        user_bp,
        url_prefix="/api/users"
    )

    app.register_blueprint(
        stock_bp,
        url_prefix="/api/stocks"
    )

    app.register_blueprint(
        search_bp,
        url_prefix="/api/search"
    )


    with app.app_context():
        # Import nécessaire pour que SQLAlchemy connaisse les modèles avant create_all
        from models import user, branch, stock

        db.create_all()


    @app.after_request
    def add_cors_headers(response):
        # CORS ouvert à tous les domaines : à restreindre avant mise en production
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response


    return app


if __name__ == "__main__":
    # Lancement en local uniquement : le serveur de dev Flask, pas pour la prod
    app = create_app()

    app.run(
        debug=True,
        port=5050
    )
