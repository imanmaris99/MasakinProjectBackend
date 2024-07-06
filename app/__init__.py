from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.utils.db import db, migrate
from app.models import users
from app.controllers.user import user_route
from dotenv import load_dotenv
from flask_cors import CORS
import os

# Initializing Flask application
app = Flask(__name__)

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

# # Registering blueprints
app.register_blueprint(user_route.user_blueprint, url_prefix='/user')

# Defining routes here
@app.route('/')
def index():
    return jsonify({'message': 'Access available !!!'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)