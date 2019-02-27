from flask_sqlalchemy import SQLAlchemy
import datetime

from app import db
import app.profile.models


class Call(db.Model):
    """Table for all the Calls for proposals
    """
    __tablename__ = "calls"

    # Meta information about the call
    id = db.Column(db.Integer, primary_key=True)
    date_published = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.relationship("User", backref="calls_published")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Actual content of the call
    information = db.Column(db.String)
    target_group = db.Column(db.String)
    proposal_template = db.Column(db.String)
    deadline = db.Column(db.DateTime)

class Proposal(db.Model):
    """The table containing all proposals
    The table is designed according to the specification in Briefing 3
    It is assumed that co-applicants will have a Researcher account on the system
    """

    __tablename__ = "proposals"

    id = db.Column(db.Integer, primary_key=True)
    call = db.relationship("Call", backref="proposals")
    call_id = db.Column(db.Integer, db.ForeignKey("calls.id"))
    researcher = db.relationship("Researcher", backref="proposals_submitted")
    researcher_id = db.Column(db.Integer, db.ForeignKey("researchers.user_id"))
    date_applied = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    title = db.Column(db.String)
    duration = db.Column(db.Integer) # Duration of the award requested (in months)
    nrp = db.Column(db.String()) # National Research Priority Area, limited to certain options
    legal_remit = db.Column(db.String) # Description of how proposal is alligned with SFI's legal remit
    ethical_issues = db.Column(db.String) # Statement concerning ethical issues

    location = db.Column(db.String) # Applicants country at time of the submission
    co_applicants = db.Column(db.String) # A list of co-applicant, if applicable
    # A list of collaborators, if applicable # collaborators is defined as a relationship in the collaborators table
    collaborators = db.Column(db.String)
    scientific_abstract = db.Column(db.String) # Scienctific abstract, max 200 words
    lay_abstract = db.Column(db.String) # Lay abstact, max 100 words

    # Programme documents - to be uploaded as a .pdf file
    # These columns relate to information needed by the 
    # flask_uploads extension to store and retrieve the 
    # file
    programme_docs_filename = db.Column(db.String)
    programme_docs_url = db.Column(db.String)

# class Collaborator(db.Model):
#     """Table for all collaborators
    
#     This table has a "many to one" relationship with the proposal table (ie many collaborators
#     relate to one proposal). See https://www.codementor.io/sheena/understanding-sqlalchemy-cheat-sheet-du107lawl 
#     for info on how this works.
#     """
#     __tablename__ = "collaborators"

#     id = db.Column(db.Integer, primary_key=True)
#     proposal = db.relationship("Proposal", backref="collaborators")
#     proposal_id = db.Column(db.Integer, db.ForeignKey("proposals.id"))

#     name = db.Column(db.String)
#     organization = db.Column(db.String)
#     email = db.Column(db.String)