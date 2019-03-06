from flask_sqlalchemy import SQLAlchemy
import datetime

from app import db
import app.profile.models


class Call(db.Model):
    """The data model for a call for proposals
    
    This has been updated to include information about calls in Briefing 4
    """

    __tablename__ = "calls"

    # Meta information about the call
    id = db.Column(db.Integer, primary_key=True)
    date_published = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey("admins.user_id"))
    admin = db.relationship("Admin", backref="calls_made")

    # Actual content of the call
    information = db.Column(db.String)
    target_group = db.Column(db.String)
    
    proposal_template_url = db.Column(db.String)
    proposal_template_filename = db.Column(db.String)

    deadline = db.Column(db.DateTime)

    eligibility_criteria = db.Column(db.String)
    duration_of_award = db.Column(db.String)
    reporting_guidelines = db.Column(db.String)
    expected_start_date = db.Column(db.String)

    status = db.Column(db.String)
    """
    Status possible values
    -----------------------
    "PUBLISHED" - The call has been published and is accepting proposals
    "FINISHED" - The call is over and not accepting proposals
    "EDIT" - The call was in process of being made, and the admin saved it for later
    """

    # The applications associated with the call (specified as backref in Proposal)

class Proposal(db.Model):
    """The table containing all proposals
    
    The table is designed according to the specification in Briefing 3
    """

    __tablename__ = "proposals"

    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey("calls.id"))
    call = db.relationship("app.call_system.models.Call", backref="proposals")
    researcher = db.relationship("Researcher", backref="proposals")
    researcher_id = db.Column(db.Integer, db.ForeignKey("researchers.user_id"))
    datetime_applied = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.String, default="PENDING ADMIN 1")
    # "reviewers" specified as a relationship backref in the "reviewers" table
    """
    "PENDING ADMIN 1" - Researcher has submitted the grant and is waiting for admin to assign reviewers
    "PENDING REVIEWER" - Reviewer must review it and accept or decline
    "APPROVED" - The admin has approved the proposal and granted a reward
    "PENDING ADMIN 2" - All reviews have approved the proposal, an admin can now approve the grant
    "REJECTED" - The proposal was rejected either by reviewer or admin
    "EDIT" - The proposal is not fully finished by the researcher and has not been submitted
    """

    title = db.Column(db.String)
    duration = db.Column(db.Integer) # Duration of the award requested (in months)
    nrp = db.Column(db.String()) # National Research Priority Area, limited to certain options
    legal_remit = db.Column(db.String) # Description of how proposal is alligned with SFI's legal remit
    ethical_issues = db.Column(db.String) # Statement concerning ethical issues

    location = db.Column(db.String) # Applicants country at time of the submission
    co_applicants = db.Column(db.String, nullable=True) # A list of co-applicant emails, if applicable
    collaborators = db.Column(db.String, nullable=True) # A list of collaborators, if applicable
    scientific_abstract = db.Column(db.String) # Scienctific abstract, max 200 words
    lay_abstract = db.Column(db.String) # Lay abstact, max 100 words

    # Programme documents - to be uploaded as a .pdf file
    # These columns relate to information needed by the 
    # flask_uploads extension to store and retrieve the 
    # file
    programme_docs_filename = db.Column(db.String)
    programme_docs_url = db.Column(db.String)
    approved = db.Column(db.String)

#class collaborators

from app.admin.models import *