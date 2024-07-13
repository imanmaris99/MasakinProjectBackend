from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.ingredient_details import IngredientDetails
from app.models.ingredient_name import IngredientName
from app.models.users import User
from app.utils.db import db
from sqlalchemy import func

ingredient_detail_blueprint = Blueprint('ingredient_detail_endpoint', __name__)

# Endpoint untuk mendapatkan daftar komposisi (GET)
@ingredient_detail_blueprint.route("/all", methods=["GET"])
def get_list_ingredients():
    try:
        ingredient_details = IngredientDetails.query.all()
        ingredient_detail_data = [ingredient.as_dict() for ingredient in ingredient_details]
        return jsonify(ingredient_detail_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
# Endpoint untuk mendapatkan daftar bahan (GET)
@ingredient_detail_blueprint.route("/all/database", methods=["GET"])
def get_list_ingredient_database():
    try:
        ingredient_names = IngredientName.query.all()
        ingredient_name_data = [ingredient_name.as_dict() for ingredient_name in ingredient_names]
        return jsonify(ingredient_name_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@ingredient_detail_blueprint.route("/new_ingredient", methods=["POST"])
@jwt_required()
def create_ingredients():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id).first()

        # Pengecekan apakah pengguna adalah admin
        if current_user.role != 'admin':
            return jsonify({"message": "Unauthorized access"}), 403

        data = request.json

        # Validasi input
        required_fields = ['recipe_id','ingredient_name_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Membuat objek recipe baru
        new_ingredient = IngredientDetails(
            recipe_id=data["recipe_id"],
            ingredient_name_id=data["ingredient_name_id"],
            dose = data.get("dose",None),

        )

        # Menambahkan dan menyimpan objek ke dalam database
        db.session.add(new_ingredient)
        db.session.commit()

        # Menyusun data respons
        response_data = new_ingredient.as_dict()

        # Mengembalikan respons dengan status 201
        return jsonify(response_data), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500