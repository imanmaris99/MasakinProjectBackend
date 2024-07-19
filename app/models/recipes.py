from sqlalchemy import ARRAY, DateTime, func
from app.models.cooking_utensils import CookingUtensils
from app.models.country import Country
from app.models.how_to_cook import HowToCooks
from app.models.ingredient_details import IngredientDetails
from app.models.rating_recipe import RatingRecipe
from app.utils.db import db

class Recipes(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_name = db.Column(db.String(255), nullable=True)
    food_image = db.Column(db.String(255), nullable=True)
    food_info = db.Column(ARRAY(db.Text), nullable=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    instructions = db.Column(ARRAY(db.Text), nullable=True)
    servings= db.Column(db.Integer, nullable=False)
    cooking_video = db.Column(db.String(255), nullable=True)
    cooking_time = db.Column(db.Integer, nullable=False) 
    dificultly_level = db.Column(db.Integer, nullable=False)
    source_of = db.Column(db.String(255), nullable=True)
    writen_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    country = db.relationship("Country", backref=db.backref("recipe", lazy=True))
    user = db.relationship("User")
    ingredientdetails = db.relationship("IngredientDetails", back_populates="recipe", cascade="all, delete-orphan")
    cooking_utensils = db.relationship("CookingUtensils", back_populates="recipe", cascade="all, delete-orphan")
    howtocooks = db.relationship("HowToCooks", back_populates="recipe", cascade="all, delete-orphan")



    def average_rating(self):
        # Hitung rata-rata rating untuk resep ini
        avg_rating = db.session.query(func.avg(RatingRecipe.rating)).filter_by(recipe_id=self.id).scalar()
        return round(avg_rating, 1) if avg_rating is not None else 0.0  # Mengembalikan 0.0 jika tidak ada rating   

    def get_ingredient_details(self):
        ingredientdetail_info = IngredientDetails.query.filter_by(recipe_id=self.id).all()
        ingredient_info_list = [ingredientdetail.updated_view() for ingredientdetail in ingredientdetail_info]
        return ingredient_info_list
    
    def get_cooking_utensil(self):
        cooking_utensil_info = CookingUtensils.query.filter_by(recipe_id=self.id).all()
        cooking_utensil_info_list = [cooking_utensil.as_update() for cooking_utensil in cooking_utensil_info] 
        return cooking_utensil_info_list
    
    def get_how_to_cook(self):
        how_to_cook_info = HowToCooks.query.filter_by(recipe_id=self.id).order_by(HowToCooks.id).all()
        how_to_cook_info_list = [howtocooks.updated_view() for howtocooks in how_to_cook_info] 
        return how_to_cook_info_list

    def as_dict(self):
        # # Dapatkan semua info negara berdasarkan country_id
        # country_info = Country.query.filter_by(id=self.country_id).all()
        # countries_list = [country.as_dict() for country in country_info] 

        return{
            "id": self.id,
            "food_name": self.food_name,
            "food_image": self.food_image,
            "food_info": self.food_info,
            # "country_id": self.country_id,
            # "country_info": countries_list,
            "country_name": self.country.country_name,
            "serving": self.servings,
            "ingredient_info": self.get_ingredient_details() if self.get_ingredient_details() else None,
            "utensil_info": self.get_cooking_utensil() if self.get_cooking_utensil() else None,
            "how_to_cook_info": self.get_how_to_cook() if self.get_how_to_cook() else None,
            "instructions" : self.instructions,
            "cooking_video": self.cooking_video,
            "cooking_time" : self.cooking_time,
            "dificultly_level" : self.dificultly_level,
            'source_of': self.source_of,
            # 'writen_by': self.writen_by,
            'written_by_name': self.user.username if self.user else None,
            "rating": self.average_rating(), # Menggunakan self.average_rating() untuk mendapatkan nilai rata-rata rating
            "created_at": self.created_at.isoformat(),  # Format ISO datetime string
            "updated_at": self.updated_at.isoformat() if self.updated_at else None  # Format ISO datetime string or None
        }
    

    def simple_view(self):
        # Dapatkan semua info negara berdasarkan country_id
        # country_info = Country.query.filter_by(id=self.country_id).all()
        # countries_list = [country.as_dict() for country in country_info] 

        return{
            "id": self.id,
            "food_name": self.food_name,
            "food_image": self.food_image,
            # "country_id": self.country_id,
            "country_name": self.country.country_name,
            "cooking_video": self.cooking_video,
            "cooking_time" : self.cooking_time,
            "dificultly_level" : self.dificultly_level,
            "rating": self.average_rating(), # Menggunakan self.average_rating() untuk mendapatkan nilai rata-rata rating
            'written_by_name': self.user.username if self.user else None,            
            "created_at": self.created_at.isoformat(),  # Format ISO datetime string
            "updated_at": self.updated_at.isoformat() if self.updated_at else None  # Format ISO datetime string or None
        }





        # # Dapatkan semua info komposisi berdasarkan ingredients
        # ingredientdetail_info = IngredientDetails.query.filter_by(id=self.id).scalar()
        # ingredient_info_list = [ingredientdetail.as_dict() for ingredientdetail in ingredientdetail_info] 

        # # Dapatkan semua info alat masak berdasarkan utensils
        # cooking_utensil_info = CookingUtensils.query.filter_by(id=self.id).scalar()
        # cooking_utensil_info_list = [cooking_utensil.as_dict() for cooking_utensil in cooking_utensil_info] 

        # # Dapatkan semua info cara memasak dan typenya berdasarkan how_to_cook
        # how_to_cook_info = HowToCooks.query.filter_by(id=self.id).scalar()
        # how_to_cook_info_list = [howtocooks.as_dict() for howtocooks in how_to_cook_info] 

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

