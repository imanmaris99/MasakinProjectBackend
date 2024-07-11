from flask import Blueprint, jsonify, request
from app.utils.db import db
from sqlalchemy import func

ingredient_detail_blueprint = Blueprint('ingredient_detail_endpoint', __name__)