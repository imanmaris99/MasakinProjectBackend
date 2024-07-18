from sqlalchemy import DateTime, func
from app.models.ingredient_name import IngredientName
from app.utils.db import db

class IngredientDetails(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    ingredient_name_id = db.Column(db.Integer, db.ForeignKey('ingredient_name.id'), nullable=False)
    dose = db.Column(db.String(25), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  

    recipe = db.relationship("Recipes", back_populates="ingredientdetails")
    ingredientname = db.relationship("IngredientName")

    def as_dict(self):
        # Dapatkan semua info bahan berdasarkan ingredient_name_id
        ingredient_name_info = IngredientName.query.filter_by(id=self.ingredient_name_id).all()
        ingredient_name_info_list = [ingredient_name.simple_view() for ingredient_name in ingredient_name_info] 

        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'ingredient_name_info': ingredient_name_info_list if ingredient_name_info_list else None,
            'ingredient_name': self.ingredientname.name,
            'ingredient_name_id': self.ingredient_name_id,
            'dose': self.dose,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def updated_view(self):
        return{
            'recipe_id': self.recipe_id,
            'ingredient_name': self.ingredientname.name,
            'ingredient_image': self.ingredientname.image,
            'ingredient_info': self.ingredientname.info,
            'dose': self.dose,
        }