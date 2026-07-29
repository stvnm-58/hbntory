# Instance SQLAlchemy partagée par toute l'app (liée à Flask dans app.py)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
