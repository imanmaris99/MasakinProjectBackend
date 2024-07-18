from sqlalchemy import ARRAY, DateTime, func
from app.models.cooking_type import CookingType
from app.utils.db import db

class HowToCooks(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=True)
    instructions= db.Column(ARRAY(db.Text), nullable=True)
    image = db.Column(ARRAY(db.Text), nullable=True)
    cooking_type_id = db.Column(db.Integer, db.ForeignKey('cooking_type.id'), nullable=True)
    cooking_type_ids = db.Column(ARRAY(db.Integer), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    recipe = db.relationship("Recipes", back_populates='howtocooks')
    cookingtype = db.relationship("CookingType")

    def as_dict(self):
        # Dapatkan semua info type masak berdasarkan cooking_type_id
        cookingtype_name = CookingType.query.filter_by(id=self.cooking_type_id).all()
        cookingtype_name_list = [cookingtype.simple_view() for cookingtype in cookingtype_name] 

        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'instructions': self.instructions,
            'image': self.image,
            'cooking_type_info': cookingtype_name_list if cookingtype_name_list else None,
            'cooking_type_id': self.cooking_type_id,
            'cooking_type_ids': self.cooking_type_ids,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }   