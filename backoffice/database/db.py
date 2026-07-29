# Instance SQLAlchemy partagée par toute l'app, liée à Flask via
# db.init_app(app) dans app.py (create_app)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
