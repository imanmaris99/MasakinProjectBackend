from app.utils.db import db

class Users(db.Model):

    # __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=True)
    # email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=True)
    # created_at
    # updated_at

def as_dict(self):
    return{
        "id": self.id,
        "username": self.username,
        "firstname": self.firstname,
        "lastname": self.lastname,
        # "email": self.email,
        "password": self.password,
        "role": self.role
    }