from datetime import datetime
from food_recommendation import db


class User(db.Model):
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120),primary_key=True, unique=True, nullable=False)
    city = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.city}')"
