from flask_login import UserMixin
from sqlalchemy import ForeignKey

from .extensions import db

user_files = db.Table('user_files', 
    db.Column('user_id', db.Integer(), ForeignKey('users.id')), 
    db.Column('file_id', db.Integer(), ForeignKey('files.id')) 
)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False) 
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    my_files = db.relationship('File', secondary=user_files, backref='myfiles')

class ImageProfile(db.Model):
    __tablename__ = "image_profile"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)  # Set as primary key
    name = db.Column(db.String(250), nullable=False)

class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=250), nullable=False)