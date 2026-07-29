from flask_sqlalchemy import SQLAlchemy

# Instance partagée, liée à l'app via db.init_app() dans app.py
db = SQLAlchemy()
