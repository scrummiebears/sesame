from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.profile.models import *

import datetime

class Reviewer(db.Model):
    """Table for reviewers

    Reviewers can be either already registered researchers, or random people that dont have an account with the system
    In the interest of time, it works like this:

    Admin selects a reviewer by email.
    The reviewer gets an email with login details (A username and password)
    The reviewer logs in to the website via a special reviewer login. (looks the same as regular login but asks for username instead of the email)
    They login, and go straight to the proposal they have to review
    They can put in comments if they want.
    They take an action - either 
        accept the proposal, and submit their comments,
        reject the poprosal, and submit their comments,
        or they save the state of their review (ie their comments on that review) and logout, to come back later and finish it

    If they choose accept or reject, their review is considered complete and they cannot log back in.
    If they choose save, they can log back in to make a decision later.
    
    """
    __tablename__ = "reviewers"

    id = db.Column(db.Integer, primary_key=True)

    login_token = db.Column(db.String)

    email = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    proposal = db.relationship("Proposal", backref="reviews")
    proposal_id = db.Column(db.Integer, db.ForeignKey("proposals.id"))
    datetime_created = db.Column(db.DateTime, default=datetime.datetime.now())

    comments = db.Column(db.String)
    completed = db.Column(db.Boolean, default=False)
    decision = db.Column(db.String)
    """
    Maybe decision is either ACCEPTED or REJECTED
    """
