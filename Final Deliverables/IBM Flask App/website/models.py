from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vmodel=db.Column(db.String(100))
    distance = db.Column(db.Float)
    speed = db.Column(db.Float)
    temp_inside = db.Column(db.Float)
    temp_outside = db.Column(db.Float)
    gas_type = db.Column(db.Integer)
    ac = db.Column(db.Integer)
    rain = db.Column(db.Integer)
    sun = db.Column(db.Integer)
    consume = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(30))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    rating = db.Column(db.Integer)
    text = db.Column(db.String(300))
    predictions = db.relationship('Prediction')


