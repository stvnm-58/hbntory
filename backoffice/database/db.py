# Instance SQLAlchemy partagée par toute l'app, liée à Flask via
# db.init_app(app) dans app.py (create_app)
from flask_sqlalchemy import SQLAlchemy

# Instance partagée, liée à l'app via db.init_app() dans app.py
db = SQLAlchemy()
