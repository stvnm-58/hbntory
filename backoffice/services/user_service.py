from database.db import db
from models.user import User
from werkzeug.security import generate_password_hash



def get_all_users():

    return User.query.filter_by(
        is_deleted=False
    ).all()



def get_user_by_id(user_id):

    return User.query.filter_by(
        id=user_id,
        is_deleted=False
    ).first()



def create_user(data):

    user = User(
        email=data["email"],
        password_hash=generate_password_hash(
            data["password"]
        ),
        role=data["role"],
        branch_id=data.get("branch_id"),
        is_deleted=False
    )


    db.session.add(user)
    db.session.commit()

    return user



def update_user(user_id, data):

    user = get_user_by_id(user_id)

    if not user:
        return None


    if "email" in data:
        user.email = data["email"]

    if "role" in data:
        user.role = data["role"]

    if "branch_id" in data:
        user.branch_id = data["branch_id"]


    db.session.commit()

    return user



def delete_user(user_id):

    user = get_user_by_id(user_id)

    if not user:
        return False


    # Soft delete demandé dans le projet
    user.is_deleted = True

    db.session.commit()

    return True