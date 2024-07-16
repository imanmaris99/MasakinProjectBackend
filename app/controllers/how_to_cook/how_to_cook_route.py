from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.cooking_type import CookingType
from app.models.how_to_cook import HowToCooks
from app.models.users import User
from app.utils.db import db
from sqlalchemy import func

how_to_cook_blueprint = Blueprint('how_to_cook_endpoint', __name__)

@how_to_cook_blueprint.route("/all", methods=["GET"])
def get_list_cook_type():
    try:
        cook_details = HowToCooks.query.all()
        cook_type_data = [cook.as_dict() for cook in cook_details]
        return jsonify(cook_type_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@how_to_cook_blueprint.route("/recipe_id/<int:recipe_id>", methods=["GET"])
def get_howtocook_list_by_recipe_id(recipe_id):
    try:
        howtocook_list = HowToCooks.query.filter_by(recipe_id=recipe_id).all()
        if howtocook_list:
            return jsonify([howtocook.as_dict() for howtocook in howtocook_list]), 200
        else:
            return jsonify({"message: recipe_id not found"}), 404
        
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@how_to_cook_blueprint.route("/all/database", methods=["GET"])
def get_detail_cooking_type():
    try:
        type_details = CookingType.query.all()
        type_data = [type.as_dict() for type in type_details]
        return jsonify(type_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@how_to_cook_blueprint.route("/new_cook_type", methods=["POST"])
@jwt_required()
def create_how_to_cook():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id).first()

        # Pengecekan apakah pengguna adalah admin
        if current_user.role != 'admin':
            return jsonify({"message": "Unauthorized access"}), 403

        data = request.json

        # Validasi input
        required_fields = ['recipe_id','cooking_type_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Membuat objek recipe baru
        new_cook_type = HowToCooks(
            recipe_id=data["recipe_id"],
            cooking_type_id=data["cooking_type_id"],
            cooking_type_ids = data.get("cooking_type_ids",None),
            instructions = data.get("instructions",None),
            image = data.get("image",None)
        )

        # Menambahkan dan menyimpan objek ke dalam database
        db.session.add(new_cook_type)
        db.session.commit()

        # Menyusun data respons
        response_data = new_cook_type.as_dict()

        # Mengembalikan respons dengan status 201
        return jsonify(response_data), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500