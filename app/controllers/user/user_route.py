from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from app.utils.helper import generate_reset_token,verify_reset_token,send_reset_email
from flask_bcrypt import Bcrypt
from app.utils.db import db
from app.models.users import User
import os

user_blueprint = Blueprint('user_endpoint', __name__)
bcrypt = Bcrypt()

# coba koneksifitas CRUD ke database via supabase--------
# sementara dan bisa berubah

@user_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_list_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()

        # Cek jika pengguna ditemukan dan jika pengguna adalah admin
        if user is None:
            return jsonify({"message": "User not found"}), 401  # Unauthorized jika pengguna tidak ditemukan

        if user.role != 'admin':
            return jsonify({"message": "You are not authorized to view this resource"}), 401  # Unauthorized jika bukan admin
        
        users = User.query.all()
        user_data = [user.as_dict() for user in users]
        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@user_blueprint.route("/register", methods=["POST"])
def create_user():
    try:
        data = request.json
        # Validasi input
        required_fields = ['username', 'firstname', 'lastname', 'email', 'phone', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400
        
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        
        new_user = User(username=data["username"],
                        firstname=data["firstname"],
                        lastname=data["lastname"],
                        email=data["email"],
                        facebook=data.get("facebook", None),
                        google=data.get("google", None),
                        phone=data["phone"],
                        password=hashed_password,
                        role='member')
        
        db.session.add(new_user)
        db.session.commit()

        # Menyusun data respons
        response_data = new_user.as_dict()

        # Mengembalikan respons dengan status 201
        return jsonify(response_data), 201

        # registration_data = {
        #     'id': new_user.id,
        #     'email': new_user.email,
        #     'username': new_user.username,
        #     "phone": new_user.phone,
        #     'role': new_user.role,
        #     'created_at': new_user.created_at.isoformat(),
        #     'updated_at': new_user.updated_at.isoformat() if new_user.updated_at else None
        # }
        # return jsonify(registration_data), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@user_blueprint.route('/login', methods=["POST"])
def login_user():
    data = request.json
    try:
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@user_blueprint.route("/profile", methods=["GET"])
@jwt_required()
def create_user_profile():
    try:
        current_user_id = get_jwt_identity()

        user = User.query.filter_by(id=current_user_id).first()

        if not user:
            return jsonify({"message":"User not found"}), 404
        
        user_data = {
           "my_profile" : user.as_dict(),
           "password" : user.password
        }

        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({"message": str(e)}),500


@user_blueprint.route('/edit', methods=["PUT"])
@jwt_required()  # Membutuhkan token JWT untuk akses
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()

        if user:
            data = request.json
            required_fields = ['username', 'firstname', 'lastname', 'email', 'facebook', 'google', 'phone']
            for field in required_fields:
                if field not in data:
                    setattr(user, field, data[field])

            db.session.commit()
            response_data = user.as_dict()

            return jsonify(response_data),200
            
        else:
            return jsonify({"message":"User not found"})

    except Exception as e:
        return jsonify({"message":str(e)}),500

# # forgot password routes (code by Prass)
# @user_blueprint.route('/forgot_password', methods=["POST"])
# def forgot_password():
#     data = request.json
#     email = data.get('email')
    
#     user = User.query.filter_by(email=email).first()
#     if user:
#         token = generate_reset_token(user.id)
#         send_reset_email(user, token)
#         return jsonify({"message": "Password reset link has been sent to your email"}), 200
#     else:
#         return jsonify({"message": "User with this email does not exist"}), 404

# #reset password routes
# @user_blueprint.route('/reset_password/<token>', methods=["POST"])
# def reset_password(token):
#     data = request.json
#     new_password = data.get('password')
    
#     user_id = verify_reset_token(token)
#     if not user_id:
#         return jsonify({"message": "Invalid or expired token"}), 400

#     user = User.query.get(user_id)
#     if user:
#         hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
#         user.password = hashed_password
#         db.session.commit()
#         return jsonify({"message": "Password has been reset"}), 200
#     else:
#         return jsonify({"message": "User not found"}), 404

#ADMIN-->>>>
# @user_blueprint.route("/register/admin", methods=["POST"])
# def create_user_admin():
#     try:
#         data = request.json
#         # Validasi input
#         required_fields = ['username', 'firstname', 'lastname', 'email', 'phone', 'password']
#         for field in required_fields:
#             if field not in data:
#                 return jsonify({"message": f"Missing field: {field}"}), 400
        
#         hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        
#         new_user_admin = User(username=data["username"],
#                         firstname=data["firstname"],
#                         lastname=data["lastname"],
#                         email=data["email"],
#                         facebook=data.get("facebook", None),
#                         google=data.get("google", None),
#                         phone=data["phone"],
#                         password=hashed_password,
#                         role='admin')
        
#         db.session.add(new_user_admin)
#         db.session.commit()

#         # Menyusun data respons
#         response_data = new_user_admin.as_dict()

#         # Mengembalikan respons dengan status 201
#         return jsonify(response_data), 201

#     except KeyError as e:
#         return jsonify({"message": f"Missing key: {str(e)}"}), 400
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500
    
@user_blueprint.route("/register/admin", methods=["POST"])
@jwt_required()
def create_user_admin():
    try:
        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Querying untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()
        
        if user.role != 'admin':
            return jsonify({"message": "Only admins can create other admin users"}), 403
        
        data = request.json
        # Validasi input
        required_fields = ['username', 'firstname', 'lastname', 'email', 'phone', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400
        
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        
        new_user_admin = User(username=data["username"],
                        firstname=data["firstname"],
                        lastname=data["lastname"],
                        email=data["email"],
                        facebook=data.get("facebook", None),
                        google=data.get("google", None),
                        phone=data["phone"],
                        password=hashed_password,
                        role='admin')
        
        db.session.add(new_user_admin)
        db.session.commit()

        # Menyusun data respons
        response_data = new_user_admin.as_dict()

        # Mengembalikan respons dengan status 201
        return jsonify(response_data), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@user_blueprint.route('/delete/<int:user_id>', methods=["DELETE"])
@jwt_required()  # Membutuhkan token JWT untuk akses
def delete_profile(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id).first()

        # Pengecekan apakah pengguna adalah admin
        if current_user.role != 'admin':
            return jsonify({"message": "Unauthorized access"}), 403

        user = User.query.get(user_id)

        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User profile deleted successfully"}), 200
        else:
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500