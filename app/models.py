from flask_login import UserMixin

from .extensions import db

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False) 
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    images = db.relationship("Image", backref="user", lazy="dynamic")  # Define the relationship

class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    type_image = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class ImageProfile(db.Model):
    __tablename__ = "image_profile"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)  # Set as primary key
    name = db.Column(db.String(250), nullable=False)