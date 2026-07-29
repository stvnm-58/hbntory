# Ré-exporte les fonctions de tous les controllers pour pouvoir écrire
# `from controllers import login, get_users, ...` depuis les routes
from .auth_controller import *
from .user_controller import *
from .stock_controller import *