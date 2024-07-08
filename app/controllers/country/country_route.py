from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.users import User
from app.utils.db import db
from app.models.country import Country

country_blueprint = Blueprint('country_endpoint', __name__)

# coba koneksifitas CRUD ke database via supabase--------
# sementara dan bisa berubah

@country_blueprint.route("/all_countries", methods=["GET"])
def get_list_country():
    try:
        countries = Country.query.all()
        country_data = [country.as_dict() for country in countries]
        return jsonify(country_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@country_blueprint.route("/new_country", methods=["POST"])
@jwt_required()
def create_country():
    try:
        data = request.json

        # Validasi input
        required_fields = ['code', 'country_name', 'continent_name']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Query untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()

        # Memastikan hanya admin yang dapat membuat negara baru
        if user.role != 'admin':
            return jsonify({"message": "Only admins can create countries"}), 403
        
        # Membuat objek Country baru
        new_country = Country(
            code=data["code"],
            country_name=data["country_name"],
            continent_name=data["continent_name"]
        )

        # Menambahkan dan menyimpan objek ke dalam database
        db.session.add(new_country)
        db.session.commit()

        # Menyusun data respons
        registration_data = {
            "id": new_country.id,
            "code": new_country.code,
            "country_name": new_country.country_name,
            "continent_name": new_country.continent_name,
            'created_at': new_country.created_at.isoformat() if new_country.created_at else None
        }

        # Mengembalikan respons dengan status 201
        return jsonify(registration_data), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
