# Package "controllers" : contient la logique de traitement des requêtes HTTP
# (parsing des entrées, appel des services, construction des réponses JSON).
# Ce fichier ré-exporte les fonctions de chaque contrôleur pour un import
# simplifié depuis routes/ (ex: "from controllers import login" au lieu de
# "from controllers.auth_controller import login").
from .auth_controller import *     # login, register
from .user_controller import *     # get_users, get_user, update_user_controller, delete_user_controller
from .stock_controller import *    # get_stocks, get_stock_controller, create_stock_controller, ...
# Remarque : branch_controller et search_controller ne sont pas ré-exportés ici,
# leurs routes (si elles existent) les importent directement depuis leur module.
