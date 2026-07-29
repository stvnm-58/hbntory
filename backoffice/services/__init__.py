# Ré-exporte les fonctions de tous les services (couche métier / accès aux
# données) pour `from services import login_user, get_all_stocks, ...`
from .auth_service import *
from .user_service import *
from .stock_service import *
from .product_service import *
