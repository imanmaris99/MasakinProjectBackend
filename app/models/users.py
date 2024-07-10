import bcrypt
from sqlalchemy import DateTime, func
from app.utils.db import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    facebook = db.Column(db.String(100), nullable=True, unique=True)
    google = db.Column(db.String(100), nullable=True, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    ratings = db.relationship("RatingRecipe", back_populates="user", cascade="all, delete-orphan")
    
    def as_dict(self):
        return{
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            'web_accounts': [
                {'type': 'facebook', 'account': self.facebook},
                {'type': 'google', 'account': self.google},
            ],
            "facebook": self.facebook,
            "google": self.google,
            "phone": self.phone,
            "role": self.role,
            "created_at": self.created_at.isoformat(),  # ISO format string
            "updated_at": self.updated_at.isoformat() if self.updated_at else None  # ISO format string or None
        }
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))