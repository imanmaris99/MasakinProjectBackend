from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.users import User
from app.utils.db import db
from app.models.rating_recipe import RatingRecipe

ratingrecipe_blueprint = Blueprint('ratingrecipe_endpoint', __name__)

# coba koneksifitas CRUD ke database via supabase--------
# sementara dan bisa berubah

@ratingrecipe_blueprint.route("/all_rating", methods=["GET"])
def get_list_rating_recipe():
    try:
        rating_recipes = RatingRecipe.query.all()
        rating_data = [rating.as_dict() for rating in rating_recipes]
        return jsonify(rating_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@ratingrecipe_blueprint.route("/new_rating", methods=["POST"])
@jwt_required()
def create_rating_recipe():
    try:
        data = request.json

        # Validasi input
        required_fields = ['rating', 'food_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Querying untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()
        
        new_rating = RatingRecipe(
            rating=data["rating"],
            food_id=data["food_id"],
            user_id=current_user_id  # Menggunakan current_user_id yang sudah didapatkan
        )

        db.session.add(new_rating)
        db.session.commit()

        registration_data = {
            "id": new_rating.id,
            "rating": new_rating.rating,
            "food_id": new_rating.food_id,
            "user_id": new_rating.user_id,
            "created_at": new_rating.created_at.isoformat()  # Pastikan tanggal dibuat dalam format ISO
        }
        return jsonify(registration_data), 201
    
    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
