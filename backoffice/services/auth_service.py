from models.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token


def authenticate_user(email, password):

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return None

    if user.is_deleted:
        return None

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return None

    return user



def create_token(user):

    return create_access_token(
        identity=user.id
    )



def login_user(email, password):

    user = authenticate_user(
        email,
        password
    )

    if not user:
        return None


    token = create_token(user)


    return {
        "access_token": token,
        "user": user
    }
def get_user_from_token(user_id):

    user = User.query.get(user_id)

    if not user:
        return None

    if user.is_deleted:
        return None

    return user
