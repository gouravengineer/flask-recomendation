from datetime import datetime
from food_recommendation import db


class User(db.Model):
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120),primary_key=True, unique=True, nullable=False)
    city = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.city}')"

class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True,unique=True,nullable=False)
    user_id = email = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    course_type = db.Column(db.String(120), nullable=False)
    food_type = db.Column(db.String(120), nullable=False)
    dry_or_gravy = db.Column(db.String(120), nullable=False)
    suggested_food = db.Column(db.String(120),nullable=True)
    rating_of_food = db.Column(db.Integer, nullable=True)
    suggested_restaurant = db.Column(db.String(120),nullable=True)
    restaurant_rating = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.user_id}', '{self.timestamp}', '{self.timestamp}', '{self.suggested_food}', '{self.suggested_restaurant}')"
