from flask import Blueprint, jsonify, request
from app.utils.db import db
from sqlalchemy import func

how_to_cook_blueprint = Blueprint('how_to_cook_endpoint', __name__)