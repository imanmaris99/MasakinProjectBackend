from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.utils.db import db, migrate
from app.models import users,country,rating_recipe,utensil_name,ingredient_name,cooking_type,recipes,cooking_utensils,ingredient_details,how_to_cook,bookmarks
from app.controllers.user import user_route
# from app.controllers.recipe import recipe_route
# from app.controllers.recipe_detail import recipe_detail_route
from app.controllers.country import country_route
from app.controllers.rating_recipe import rating_recipe_route
from app.controllers.recipe import recipe_route
from dotenv import load_dotenv
from flask_cors import CORS
import os

# Initializing Flask application
app = Flask(__name__)

CORS(app)

load_dotenv()

# Debugging output to check environment variables
# print("DB_TYPE:", os.getenv('DB_TYPE'))
# print("DB_NAME:", os.getenv('DB_NAME'))
# print("DB_USER:", os.getenv('DB_USER'))
# print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
# print("DB_HOST:", os.getenv('DB_HOST'))
# print("DB_PORT:", os.getenv('DB_PORT'))
# print("DATABASE_URI:", os.getenv('DATABASE_URI'))

# Setting database URI directly
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initializing database
db.init_app(app)

migrate.init_app(app, db)

# # Setting JWT secret key directly
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# # Registering blueprints
app.register_blueprint(user_route.user_blueprint, url_prefix='/user')
app.register_blueprint(recipe_route.recipe_blueprint, url_prefix='/recipe')
# app.register_blueprint(recipe_route.recipe_blueprint, url_prefix='/recipe')
# app.register_blueprint(recipe_detail_route.recipe_detail_blueprint, url_prefix='/recipe_detail')
app.register_blueprint(country_route.country_blueprint, url_prefix='/country')
app.register_blueprint(rating_recipe_route.ratingrecipe_blueprint, url_prefix='/rating_recipe')

# Defining routes here
@app.route('/')
def index():
    return jsonify({'message': 'Access available !!!'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)