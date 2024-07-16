from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.cooking_utensils import CookingUtensils
from app.models.users import User
from app.models.utensil_name import UtensilName
from app.utils.db import db
from sqlalchemy import func

cooking_utensil_blueprint = Blueprint('cooking_utensil_endpoint', __name__)

@cooking_utensil_blueprint.route("/all", methods=["GET"])
def get_list_cooking_utensil():
    try:
        cook_utensil_details = CookingUtensils.query.all()
        cook_utensil_data = [cook_utensil.as_dict() for cook_utensil in cook_utensil_details]
        return jsonify(cook_utensil_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@cooking_utensil_blueprint.route("/recipe_id/<int:recipe_id>", methods=["GET"])
def get_utensil_lists_by_recipe_id(recipe_id):
    try:
        utensil_list = CookingUtensils.query.filter_by(recipe_id=recipe_id).all()
        if utensil_list:
            return jsonify([utensil.as_dict() for utensil in utensil_list]), 200
        else:
            return jsonify({"message: recipe_id not found"}), 404
        
    except Exception as e:
        return jsonify({"message": str(e)}), 500
        
@cooking_utensil_blueprint.route("/all/database", methods=["GET"])
def get_list_utensil_database():
    try:
        utensil_name_details = UtensilName.query.all()
        utensil_name_data = [utensil_name.as_dict() for utensil_name in utensil_name_details]
        return jsonify(utensil_name_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@cooking_utensil_blueprint.route("/new_cooking_utensil", methods=["POST"])
@jwt_required()
def create_new_cooking_utensil():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id).first()

        # Pengecekan apakah pengguna adalah admin
        if current_user.role != 'admin':
            return jsonify({"message": "Unauthorized access"}), 403

        data = request.json

        # Validasi input
        required_fields = ['recipe_id','utensil_name_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Membuat objek recipe baru
        new_cooking_utensil = CookingUtensils(
            recipe_id=data["recipe_id"],
            utensil_name_id=data["utensil_name_id"],
        )

        # Menambahkan dan menyimpan objek ke dalam database
        db.session.add(new_cooking_utensil)
        db.session.commit()

        # Menyusun data respons
        response_data = new_cooking_utensil.as_dict()

        # Mengembalikan respons dengan status 201
        return jsonify(response_data), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500