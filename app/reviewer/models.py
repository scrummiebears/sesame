from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.profile.models import *

import datetime

class Reviewer(db.model):
    __tablename__ = "reviewers"

    researcher = db.relationship("Researcher", backref="reviews")
    researcher_id = db.Column(db.Integer, db.ForeignKey("researchers.user_id"))

    comments = db.Column(db.String)
    completed = db.Column(db.Boolean)
    decision = db.Column(db.String)
    """
    Maybe decision is either ACCEPTED or REJECTED
    """