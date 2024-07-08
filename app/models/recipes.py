from sqlalchemy import DateTime, func
from app.models.rating_recipe import RatingRecipe
from app.utils.db import db

class Recipe(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    food_info = db.Column(db.Text, nullable=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    country = db.relationship("Country")
    food = db.relationship("Food")

    def average_rating(self):
        # Hitung rata-rata rating untuk resep ini
        avg_rating = db.session.query(func.avg(RatingRecipe.rating)).filter_by(food_id=self.id).scalar()
        return avg_rating if avg_rating is not None else 0.0  # Mengembalikan 0.0 jika tidak ada rating    

    def as_dict(self):
        return{
            "id": self.id,
            "food_id": self.food_id,
            "food_info": self.food_info,
            "country_id": self.country_id,
            "country": self.country.as_dict() if self.country else None,
            "rating": self.average_rating(), # Menggunakan self.average_rating() untuk mendapatkan nilai rata-rata rating
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    

    # country = db.relationship('Country', backref=db.backref('recipe', lazy=True))
    # food = db.relationship('Food', backref=db.backref('recipe'))
    # ratings = db.relationship("RatingRecipe", back_populates="recipe")

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

