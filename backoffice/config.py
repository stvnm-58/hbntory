import os
from dotenv import load_dotenv

# Charge les variables du fichier .env dans l'environnement du process
load_dotenv()


class Config:
    # SQLite en local par défaut, surchargeable via DATABASE_URL en prod
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///hbntory.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Valeur par défaut à usage dev uniquement, ne pas garder en prod
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "dev-secret-key"
    )

    # URL du microservice produits externe utilisé par product_service/search_service
    PRODUCT_API_URL = os.getenv(
        "PRODUCT_API_URL",
        "http://localhost:5001"
    )
