from sqlalchemy import DateTime, func
from app.utils.db import db

class Recipe(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_name = db.Column(db.String(100), nullable=False)
    food_image = db.Column(db.String(100), nullable=True)
    food_info = db.Column(db.Text, nullable=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    country = db.relationship('Country', backref=db.backref('recipes', lazy=True))


    def as_dict(self):
        return{
            "id": self.id,
            "food_name": self.food_name,
            "food_image": self.food_image,
            "food_info": self.food_info,
            "country_id": self.country_id,
            "country": self.country.as_dict() if self.country else None,
            "rating": self.rating,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    # //menampilkan nilai rerata di
    # SELECT food_name, AVG(score) AS average_score
    # FROM rating_table
    # GROUP BY food_name;

    # //akses country dari recipe
    # recipe = Recipe.query.first()
    # print(recipe.country.country_name)  # Mengakses nama negara dari resep

    # //akses recipe dari country
    # country = Country.query.first()
    # for recipe in country.recipes:
    #     print(recipe.food_name)  # Mengakses nama makanan dari negara

