from flask import Blueprint, jsonify, request
from app.utils.db import db
from sqlalchemy import func

cooking_utensil_blueprint = Blueprint('cooking_utensil_endpoint', __name__)