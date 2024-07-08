from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.db import db
from app.models.food import Food
from app.models.users import User
from app.models.rating_recipe import RatingRecipe
from sqlalchemy import func

food_blueprint = Blueprint('food_endpoint', __name__)

# Endpoint untuk mendapatkan daftar makanan (GET)
@food_blueprint.route("/all", methods=["GET"])
def get_list_foods():
    try:
        foods = Food.query.all()
        food_data = [food.as_dict() for food in foods]
        return jsonify(food_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@food_blueprint.route("/new_food", methods=["POST"])
@jwt_required()
def create_food():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id).first()

        # Pengecekan apakah pengguna adalah admin
        if current_user.role != 'admin':
            return jsonify({"message": "Unauthorized access"}), 403

        data = request.json

        # Validasi input
        required_fields = ['food_name']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Membuat objek Food baru
        new_food = Food(
            food_name=data["food_name"],
            food_image=data.get("food_image", None)
        )

        # Menambahkan dan menyimpan objek ke dalam database
        db.session.add(new_food)
        db.session.commit()

        # Menyusun data respons
        registration_data = {
            "id": new_food.id,
            "food_name": new_food.food_name,
            "food_image": new_food.food_image,
            "created_at": new_food.created_at.isoformat(),
            "updated_at": new_food.updated_at.isoformat() if new_food.updated_at else None
        }

        # Mengembalikan respons dengan status 201
        return jsonify(registration_data), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500