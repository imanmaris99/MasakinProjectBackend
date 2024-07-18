from sqlalchemy import DateTime, func
from app.models.utensil_name import UtensilName
from app.utils.db import db

class CookingUtensils(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=True)
    utensil_name_id = db.Column(db.Integer, db.ForeignKey('utensil_name.id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    utensilname = db.relationship("UtensilName", backref=db.backref("cooking_utensils", lazy=True))
    recipe = db.relationship("Recipes", back_populates="cooking_utensils")

    def as_dict(self):
        # Dapatkan semua info nama alat berdasarkan ingredient_name_id
        utensil_name_info = UtensilName.query.filter_by(id=self.utensil_name_id).all()
        utensil_name_info_list = [utensilname.as_dict() for utensilname in utensil_name_info] 

        
        return {
            "id": self.id,
            "recipe_id": self.recipe_id,
            "utensil_name_id": self.utensil_name_id,
            "utensil_name": utensil_name_info_list if utensil_name_info_list else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def as_update(self):
        return {
            "recipe_id": self.recipe_id,
            "utensil_name": self.utensilname.name,
            "utensil_image": self.utensilname.image,
            "utensil_info": self.utensilname.info
        }