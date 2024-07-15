
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.users import User
from app.utils.db import db
from flask import Blueprint, jsonify, request
from app.models.bookmarks import Bookmarks


bookmark_blueprint = Blueprint('bookmark_endpoint', __name__)

@bookmark_blueprint.route("/all", methods=["GET"])
def get_bookmarks():
    try:
        list_my_recipes = Bookmarks.query.all()
        list_my_recipe_data = [list_my_recipe.as_dict() for list_my_recipe in list_my_recipes]
        return jsonify(list_my_recipe_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
# Endpoint untuk mendapatkan bookmark berdasarkan recipe_id (GET)
@bookmark_blueprint.route("/user/<int:recipe_id>", methods=["GET"])
def get_bookmarks_by_user_from_recipe_id(recipe_id):
    try:
        bookmarks = Bookmarks.query.filter_by(recipe_id=recipe_id).all()
        if bookmarks:
            bookmark_data = [bookmark.as_dict() for bookmark in bookmarks]
            return jsonify(bookmark_data), 200
        else:
            return jsonify({"message": "No bookmarks found for this recipe"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Endpoint untuk mendapatkan bookmark berdasarkan user_id (GET)
@bookmark_blueprint.route("/user/<int:user_id>", methods=["GET"])
def get_bookmarks_by_user_id(user_id):
    try:
        bookmarks = Bookmarks.query.filter_by(user_id=user_id).all()
        if bookmarks:
            bookmark_data = [bookmark.as_dict() for bookmark in bookmarks]
            return jsonify(bookmark_data), 200
        else:
            return jsonify({"message": "No bookmarks found for this user"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@bookmark_blueprint.route("/new_bookmark", methods=["POST"])
@jwt_required()
def create_bookmark():
    try:
        current_user_id = get_jwt_identity()
        data = request.json

        # Validasi input
        required_fields = ['recipe_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Membuat objek bookmark baru
        new_bookmark = Bookmarks(
            recipe_id=data["recipe_id"],
            user_id=current_user_id
        )

        # Menambahkan dan menyimpan objek ke dalam database
        db.session.add(new_bookmark)
        db.session.commit()

        # Menyusun data respons
        response_data = new_bookmark.as_dict()

        # Mengembalikan respons dengan status 201
        return jsonify(response_data), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@bookmark_blueprint.route("/delete/<int:recipe_id>", methods=["DELETE"])
@jwt_required()
def delete_bookmark(recipe_id):
    try:
        current_user_id = get_jwt_identity()
        bookmark = Bookmarks.query.filter_by(recipe_id=recipe_id, user_id=current_user_id).first()
        
        if bookmark:
            db.session.delete(bookmark)
            db.session.commit()
            return jsonify({"message": "Bookmark deleted successfully"}), 200
        else:
            return jsonify({"message": "Bookmark not found"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500