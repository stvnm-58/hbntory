from flask import Flask

from config import Config
from database.db import db

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.stock_routes import stock_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)


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


    with app.app_context():

        from models import user, branch, stock

        db.create_all()


    return app



if __name__ == "__main__":

    app = create_app()

    app.run(
        debug=True,
        port=5000
    )
