# Ré-exporte l'instance SQLAlchemy partagée pour `from database import db`
from .db import db

__all__ = ["db"]
