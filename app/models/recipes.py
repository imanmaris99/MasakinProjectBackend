from sqlalchemy import DateTime, func
from app.models.cooking_utensils import CookingUtensils
from app.models.country import Country
from app.models.food import Food
from app.models.how_to_cook import HowToCooks
from app.models.ingredient_details import IngredientDetails
from app.models.rating_recipe import RatingRecipe
from app.utils.db import db

class Recipes(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    food_info = db.Column(db.Text, nullable=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    ingredients = db.Column(db.Integer, db.ForeignKey('ingredient_details.id'), nullable=True)
    utensils = db.Column(db.Integer, db.ForeignKey('cooking_utensils.id'), nullable=True)
    how_to_cook = db.Column(db.Integer, db.ForeignKey('how_to_cooks.id'), nullable=True)
    instructions= db.Column(db.Text, nullable=True)
    servings= db.Column(db.Integer, nullable=False)
    cooking_video = db.Column(db.String(255), nullable=True)
    cooking_time = db.Column(db.Integer, nullable=False) 
    dificultly_level = db.Column(db.Integer, nullable=False)
    source_of = db.Column(db.String(255), nullable=True)
    writen_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    country = db.relationship("Country")
    food = db.relationship("Food")
    user = db.relationship("User")
    ingredientdetails = db.relationship("IngredientDetails", back_populates="recipe", cascade="all, delete-orphan")
    cookingutensils = db.relationship("CookingUtensils", back_populates="recipe", cascade="all, delete-orphan")
    howtocooks = db.relationship("HowToCooks", back_populates="recipe", cascade="all, delete-orphan")



    def average_rating(self):
        # Hitung rata-rata rating untuk resep ini
        avg_rating = db.session.query(func.avg(RatingRecipe.rating)).filter_by(food_id=self.id).scalar()
        return round(avg_rating, 1) if avg_rating is not None else 0.0  # Mengembalikan 0.0 jika tidak ada rating   

    def as_dict(self):
        # Dapatkan semua info negara berdasarkan country_id
        country_info = Country.query.filter_by(id=self.country_id).all()
        countries_list = [country.as_dict() for country in country_info] 

        # Dapatkan semua info food berdasarkan food_id
        food_image = Food.query.filter_by(id=self.food_id).all()
        foods_list = [food.as_dict() for food in food_image] 

        # Dapatkan semua info komposisi berdasarkan ingredients
        ingredient_info = IngredientDetails.query.filter_by(id=self.ingredients).all()
        ingredient_info_list = [ingredient.as_dict() for ingredient in ingredient_info] 

        # Dapatkan semua info alat masak berdasarkan utensils
        utensil_info = CookingUtensils.query.filter_by(id=self.utensils).all()
        utensil_info_list = [cookingutensil.as_dict() for cookingutensil in utensil_info] 

        # Dapatkan semua info cara memasak dan typenya berdasarkan how_to_cook
        how_to_cook_info = HowToCooks.query.filter_by(id=self.how_to_cook).all()
        how_to_cook_info_list = [howtocooks.as_dict() for howtocooks in how_to_cook_info] 


        return{
            "id": self.id,
            "food_id": self.food_id,
            "food_image": foods_list,
            "food_info": self.food_info,
            "country_id": self.country_id,
            "country_info": countries_list,
            "ingredients" : self.ingredients,
            "ingredient_info": ingredient_info_list if ingredient_info_list else None,
            "utensils": self.utensils,
            "utensil_info": utensil_info_list if utensil_info_list else None,
            "how_to_cook": self.how_to_cook,
            "how_to_cook_info": how_to_cook_info_list if how_to_cook_info_list else None,
            "instructions" : self.instructions,
            "cooking_video": self.cooking_video,
            "cooking_time" : self.cooking_time,
            "dificultly_level" : self.dificultly_level,
            'source_of': self.source_of,
            'writen_by': self.writen_by,
            'user_name': self.user.name if self.user else None,
            "rating": self.average_rating(), # Menggunakan self.average_rating() untuk mendapatkan nilai rata-rata rating
            "created_at": self.created_at.isoformat(),  # Format ISO datetime string
            "updated_at": self.updated_at.isoformat() if self.updated_at else None  # Format ISO datetime string or None
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

