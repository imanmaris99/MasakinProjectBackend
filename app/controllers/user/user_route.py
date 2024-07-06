from flask import Blueprint, jsonify, request
from app.utils.db import db
from app.models.users import User

user_blueprint = Blueprint('user_endpoint', __name__)

# coba koneksifitas ke database via supabase--------
@user_blueprint.route("/", methods=["GET"])
def get_list_user():
    try:
        users = User.query.all()
        user_data = [user.as_dict() for user in users]
        return user_data , 201

    except Exception as e:
        return str(e),500

@user_blueprint.route("/", methods=["POST"])
def create_user():
    try:
        data = request.json

        new_user=User()
        new_user.username=data["username"]
        new_user.firstname=data["firstname"]
        new_user.lastname=data["lastname"]
        # new_user.email=data["email"]
        new_user.password=data["password"]
        new_user.role='member'

        db.session.add(new_user)
        db.session.commit()

        registration_data = {
            'id': new_user.id,
            # 'email': new_user.email,
            'username': new_user.username,
            'password': new_user.password,
            'role': new_user.role,
        }
        return registration_data,201

    except Exception as e:
        return str(e),500
# -------------------------------------------------------


