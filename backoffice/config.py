import os


class Config:
    """
    Configuration générale du Backoffice
    """

    # Clé utilisée par Flask pour les sessions/JWT plus tard
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key"
    )

    # Base de données locale pour le développement
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///hbntory.db"
    )

    # Désactive les notifications inutiles de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
