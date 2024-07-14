from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.db import db
from app.models.recipes import Recipes
from app.models.users import User
from app.models.rating_recipe import RatingRecipe
from sqlalchemy import func

recipe_blueprint = Blueprint('recipe_endpoint', __name__)

# Endpoint untuk mendapatkan daftar makanan (GET)
@recipe_blueprint.route("/all", methods=["GET"])
def get_list_recipes():
    try:
        recipes = Recipes.query.all()
        recipe_data = [recipe.simple_view() for recipe in recipes]
        return jsonify(recipe_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#endpoint get recipe by id 
@recipe_blueprint.route("/<int:id>", methods=["GET"])
def get_list_recipe_by_id(id):
    try:
        recipe = Recipes.query.get(id)
        if recipe :
            return jsonify(recipe.as_dict()), 200
        else :
            return jsonify({"message: recipe not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#endpoint get recipe by country 
@recipe_blueprint.route("/country/<int:country_id>", methods=["GET"])
def get_recipes_by_country_id(country_id):
    try:
        recipes = Recipes.query.filter_by(country_id=country_id).all()
        if recipes:
            recipe_data = [recipe.simple_view() for recipe in recipes]
            return jsonify(recipe_data), 200
        else:
            return jsonify({"message": "No recipes found for this country"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

#endpoint get recipe by title
@recipe_blueprint.route("/title/<string:title>", methods=["GET"])
def get_recipes_by_title(title):
    try:
        recipes = Recipes.query.filter(func.lower(Recipes.food_name).contains(func.lower(title))).all()
        if recipes:
            recipe_data = [recipe.simple_view() for recipe in recipes]
            return jsonify(recipe_data), 200
        else:
            return jsonify({"message": "No recipes found with this title"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

#endpoint create recipe
@recipe_blueprint.route("/new_recipe", methods=["POST"])
@jwt_required()
def create_recipe():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id).first()

        # Pengecekan apakah pengguna adalah admin
        if current_user.role != 'admin':
            return jsonify({"message": "Unauthorized access"}), 403

        data = request.json

        # Validasi input
        required_fields = ['food_name','country_id','instructions','servings','cooking_time','dificultly_level']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Membuat objek recipe baru
        new_recipe = Recipes(
            food_name=data["food_name"],
            food_image=data.get("food_image"),
            food_info=data.get("food_info", None),
            country_id=data["country_id"],
            instructions = data["instructions"],
            servings=data["servings"],
            cooking_video = data.get("cooking_video"),
            cooking_time = data["cooking_time"],
            dificultly_level = data["dificultly_level"],
            source_of = data.get("source_of",None),
            writen_by=data.get("writen_by")
        )

        # Menambahkan dan menyimpan objek ke dalam database
        db.session.add(new_recipe)
        db.session.commit()

        # Menyusun data respons
        response_data = new_recipe.as_dict()

        # Mengembalikan respons dengan status 201
        return jsonify(response_data), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#endpoint edit recipe
@recipe_blueprint.route("/edit/<int:recipe_id>", methods=["PUT"])
@jwt_required()
def edit_recipe(recipe_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id).first()

        # Pengecekan apakah pengguna adalah admin
        if current_user.role != 'admin':
            return jsonify({"message": "Unauthorized access"}), 403

        recipe = Recipes.query.get(recipe_id)

        if recipe:
            data = request.json

            # Validasi input
            required_fields = ['food_name','country_id','instructions','servings','cooking_time','dificultly_level']
            for field in required_fields:
                if field in data:
                    setattr(recipe, field, data[field])

            db.session.commit()

            # Menyusun data respons
            response_data = recipe.as_dict()

            # Mengembalikan respons dengan status 200
            return jsonify(response_data), 200
        else:
            return jsonify({"message": "Recipe not found"}), 404

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

#endpoint DELETE recipe by id
@recipe_blueprint.route("/delete/<int:recipe_id>", methods=["DELETE"])
@jwt_required()
def delete_recipe(recipe_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id).first()

        # Pengecekan apakah pengguna adalah admin
        if current_user.role != 'admin':
            return jsonify({"message": "Unauthorized access"}), 403

        recipe = Recipes.query.get(recipe_id)

        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return jsonify({"message": "Recipe deleted successfully"}), 200
        else:
            return jsonify({"message": "Recipe not found"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500