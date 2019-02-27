from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy.ext.declarative import declared_attr

from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(256),unique=True)
    pwd_hash = db.Column(db.String(200))
    # Need for isActive? - Only for account validation
    #is_active = db.Column(db.Boolean,default=False)
    role = db.Column(db.String(80))


    def __init__(self, email, pwd_hash, role):
        self.email = email
        self.pwd_hash = pwd_hash
        #self.is_active = is_active
        self.role = role     