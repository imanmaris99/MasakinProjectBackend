from flask import Flask, json, jsonify
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from app.utils.db import db, migrate
from app.models import users,country,rating_recipe,utensil_name,ingredient_name,cooking_type,recipes,cooking_utensils,ingredient_details,how_to_cook,bookmarks
from app.controllers.user import user_route
from app.controllers.recipe import recipe_route
from app.controllers.ingredient_detail import ingredient_detail_route
from app.controllers.how_to_cook import how_to_cook_route
from app.controllers.cooking_utensil import cooking_utensil_route
from app.controllers.country import country_route
from app.controllers.rating_recipe import rating_recipe_route
from app.controllers.bookmark import bookmark_route
from dotenv import load_dotenv
# from flask_mail import Mail
from flask_cors import CORS
import os

# Initializing Flask application
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE':'simple'})
CORS(app)
load_dotenv()

# Setting database URI directly
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initializing database
db.init_app(app)
migrate.init_app(app, db)

# # Setting JWT secret key directly
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# #Flask-mail(reset password handler) config
# app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
# app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT') or 587)
# app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') is not None
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# mail = Mail(app)

# Swagger UI Configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/openapi.json'  # Ensure this URL is correct
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Masakin API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# # Registering routes directly with Api
# api = Api(app, doc=None)  # Disable default Swagger UI route if using flask-swagger-ui

# # Registering blueprints
app.register_blueprint(user_route.user_blueprint, url_prefix='/user')
app.register_blueprint(recipe_route.recipe_blueprint, url_prefix='/recipe')
app.register_blueprint(ingredient_detail_route.ingredient_detail_blueprint, url_prefix='/ingredient')
app.register_blueprint(how_to_cook_route.how_to_cook_blueprint,url_prefix='/how_to_cook')
app.register_blueprint(cooking_utensil_route.cooking_utensil_blueprint, url_prefix='/cooking_utensil')
app.register_blueprint(country_route.country_blueprint, url_prefix='/country')
app.register_blueprint(rating_recipe_route.ratingrecipe_blueprint, url_prefix='/rating')
app.register_blueprint(bookmark_route.bookmark_blueprint, url_prefix='/bookmark')

# Defining routes here
@app.route('/')
@cache.cached(timeout=50)
def index():
    return jsonify({'message': 'Access available !!!'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)