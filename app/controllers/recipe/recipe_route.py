from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.users import User
from app.utils.db import db
from app.models.rating_recipe import RatingRecipe
from app.models.recipes import Recipe

recipe_blueprint = Blueprint('recipe_endpoint', __name__)

@recipe_blueprint.route("/all_recipes", methods=["GET"])
def get_list_recipes():
    try:
        recipes = Recipe.query.all()
        recipe_data = [recipe.as_dict() for recipe in recipes]
        return jsonify(recipe_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@recipe_blueprint.route("/new_recipe", methods=["POST"])
@jwt_required()
def create_recipe():
    try:
        data = request.json

        # Validasi input
        required_fields = ['food_id','food_info', 'country_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Querying untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()
        
        if user.role != 'admin':
            return jsonify({"message": "Only admins can create recipes"}), 403

        new_recipe = Recipe(
            food_id=data["food_id"],
            food_info=data.get("food_info", None),
            country_id=data["country_id"]
        )

        db.session.add(new_recipe)
        db.session.commit()

        # Menyusun data respons
        registration_data = {
            "id": new_recipe.id,
            "food_id": new_recipe.food_id,
            "food_info": new_recipe.food_info,
            "country_id": new_recipe.country_id,
            "created_at": new_recipe.created_at.isoformat(),
            "updated_at": new_recipe.updated_at.isoformat() if new_recipe.updated_at else None
        }

        return jsonify(registration_data), 201
    
    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
