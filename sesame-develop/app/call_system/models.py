from flask_sqlalchemy import SQLAlchemy
import datetime

from app import db
import app.profile.models


class Call(db.Model):

    __tablename__ = "calls"

    # Meta information about the call
    id = db.Column(db.Integer, primary_key=True)
    date_published = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    published_by = db.Column(db.Integer)#, db.ForeignKey("users.user_id"))

    # Actual content of the call
    information = db.Column(db.String)
    target_group = db.Column(db.String)
    proposal_template = db.Column(db.String)
    deadline = db.Column(db.DateTime)

    # The applications associated with the call
    #proposals = db.Column(db.relationship("app.call_system.models.Proposal"))

class Proposal(db.Model):
    """The table containing all proposals
    
    The table is designed according to the specification in Briefing 3
    """

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    #call = relationship("app.call_system.models.Call", back_populates="proposals")

    title = db.Column(db.String)
    duration = db.Column(db.Integer) # Duration of the award requested (in months)
    nrp = db.Column(db.String()) # National Research Priority Area, limited to certain options
    legal_remit = db.Column(db.String) # Description of how proposal is alligned with SFI's legal remit
    ethical_issues = db.Column(db.String) # Statement concerning ethical issues

    location = db.Column(db.String) # Applicants country at time of the submission
    co_applicants = db.Column(db.String, nullable=True) # A list of co-applicant emails, if applicable
    collaborators = db.Column(db.String, nullable=True) # A list of collaborators, if applicable
    scientific_abstact = db.Column(db.String) # Scienctific abstract, max 200 words
    lay_abstact = db.Column(db.String) # Lay abstact, max 100 words

    # Programme documents - to be uploaded as a .pdf file
    # These columns relate to information needed by the 
    # flask_uploads extension to store and retrieve the 
    # file
    programme_docs_filename = db.Column(db.String)
    programme_docs_url = db.Column(db.String)

#class collaborators