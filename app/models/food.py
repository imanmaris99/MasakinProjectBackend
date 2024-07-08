from sqlalchemy import DateTime, func
from app.utils.db import db

class Food(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_name = db.Column(db.String(100), nullable=False)
    food_image = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  

#   # Relationship with Recipe
#     ratings = db.relationship('RatingRecipe', back_populates='food')
    
    def as_dict(self):
        return{
            "id": self.id,
            "food_name": self.food_name,
            "food_image": self.food_image,
            "created_at": self.created_at.isoformat(),  # Format ISO datetime string
            "updated_at": self.updated_at.isoformat() if self.updated_at else None  # Format ISO datetime string or None
        }
    