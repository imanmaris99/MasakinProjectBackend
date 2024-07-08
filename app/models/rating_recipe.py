from sqlalchemy import DateTime, func
from app.utils.db import db

class RatingRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer, nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 

    food = db.relationship("Food", backref=db.backref("ratings", lazy=True))
    user = db.relationship("User", back_populates="ratings")


    def as_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "food_id": self.food_id,
            "user_id": self.user_id,
            "created_at": self.created_at
        }


    # # Relationships
    # food = db.relationship('Food', back_populates='ratings')
    # user = db.relationship('User', back_populates='ratings')
    # recipe = db.relationship('Recipe', back_populates='ratings')