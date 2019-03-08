from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.profile.models import *

import datetime

class Reviewer(db.Model):
    __tablename__ = "reviewers"

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User", backref=db.backref("admin", uselist=False))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    proposal = db.relationship("Proposal", backref="reviews")
    proposal_id = db.Column(db.Integer, db.ForeignKey("proposals.id"))
    datetime_created = db.Column(db.DateTime, default=datetime.datetime.now())

    comments = db.Column(db.String)
    completed = db.Column(db.Boolean, default=False)
    decision = db.Column(db.String)
    """
    Maybe decision is either ACCEPTED or REJECTED
    """