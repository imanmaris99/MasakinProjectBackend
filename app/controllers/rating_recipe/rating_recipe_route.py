from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import func
from app.models.country import Country
from app.models.recipes import Recipes
from app.models.users import User
from app.utils.db import db
from app.models.rating_recipe import RatingRecipe

ratingrecipe_blueprint = Blueprint('ratingrecipe_endpoint', __name__)

# coba koneksifitas CRUD ke database via supabase--------
# sementara dan bisa berubah

@ratingrecipe_blueprint.route("/all", methods=["GET"])
def get_list_rating_recipe():
    try:
        rating_recipes = RatingRecipe.query.all()
        rating_data = [rating.as_dict() for rating in rating_recipes]
        return jsonify(rating_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@ratingrecipe_blueprint.route("/new_rate", methods=["POST"])
@jwt_required()
def rate_recipe():
    try:
        current_user_id = get_jwt_identity()
        data = request.json

        # Validasi input
        required_fields = ['rating', 'recipe_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Membuat objek rating baru
        new_rating = RatingRecipe(
            rating=data["rating"],
            recipe_id=data["recipe_id"],
            user_id=current_user_id
        )

        # Menambahkan dan menyimpan objek ke dalam database
        db.session.add(new_rating)
        db.session.commit()

        return jsonify(new_rating.as_dict()), 201
    
    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@ratingrecipe_blueprint.route("/average/<int:recipe_id>", methods=["GET"])
def get_average_rating(recipe_id):
    try:
        average_rating = db.session.query(func.avg(RatingRecipe.rating)).filter_by(recipe_id=recipe_id).scalar()
        recipe = Recipes.query.filter_by(id=recipe_id).first()
        country = Country.query.filter_by(id=recipe.country_id).first()
        # if recipe is None:
        #     return jsonify({"message":"Recipe not found"}), 404

        if average_rating is not None:
            return jsonify(
                {
                "recipe_id": recipe_id, 
                "food_name": recipe.food_name,
                "country" : country.country_name,
                "average_rating": round(average_rating, 2),
                "dificulty_level": recipe.dificultly_level
                }
            ), 200
        else:
            return jsonify({"message": "No ratings found for this recipe"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500
