from sqlalchemy import DateTime, func
from app.utils.db import db

class UtensilName(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    info = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "info": self.info,
            "created_at": self.created_at.isoformat(),  # Format ISO datetime string
            "updated_at": self.updated_at.isoformat() if self.updated_at else None  # Format ISO datetime string or None
        }