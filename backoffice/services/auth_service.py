# Logique métier pour la connexion et la création de comptes utilisateurs
from models.user import User
from database.db import db

from flask_jwt_extended import create_access_token



def login_user(email, password):
    # Vérifie email/mot de passe et génère un JWT si valides, sinon None
    user = User.query.filter_by(
        email=email,
        is_deleted=False
    ).first()


    if not user:
        return None


    if not user.check_password(password):
        return None


    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )


    return {
        "token": token,
        "user": user.to_dict()
    }




def create_user(
    email,
    password,
    role="employee",
    branch_id=None
):
    # Crée un utilisateur si l'email n'est pas déjà pris, sinon renvoie None
    existing = User.query.filter_by(
        email=email
    ).first()


    if existing:
        return None



    user = User(

        email=email,

        role=role,

        branch_id=branch_id

    )


    user.set_password(password)


    db.session.add(user)

    db.session.commit()


    return user
