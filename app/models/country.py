from sqlalchemy import DateTime, func
from app.utils.db import db

class Country(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), nullable=False)
    country_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    

    def as_dict(self):
        return{
            "id": self.id,
            "code": self.code,
            "country_name": self.country_name,
            "created_at": self.created_at
        }
 