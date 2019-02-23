from flask_sqlalchemy import SQLAlchemy

from app import db
from app.auth.models import User

class Admin(db.Model):
    
    __tablename__ = "admins"

    user = db.relationship("User", backref=db.backref("admin", uselist=False))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

class Researcher(db.Model):

    __tablename__ = "researchers"

    user = db.relationship("User", backref=db.backref("researcher", uselist=False))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    prefix = db.Column(db.String, nullable=False)

    suffix = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    phone_ext = db.Column(db.String, nullable=True)
    orcid = db.Column(db.String, nullable=True)
    
class Admin(db.Model):
    __tablename__ = "admin"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    prefix = db.Column(db.String, nullable=False)

    suffix = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    phone_ext = db.Column(db.String, nullable=True)
    orcid = db.Column(db.String, nullable=True)
    

class Education(db.Model):

    __tablename__ = "educations"
    
    researcher = db.relationship("Researcher", backref="education")
    researcher_id = db.Column(db.Integer, db.ForeignKey("researchers.user_id"),
                                                       primary_key=True)
    degree = db.Column(db.String, nullable=True)
    field_of_study = db.Column(db.String, nullable=True)
    institution = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    degree_award_year = db.Column(db.String, nullable=True)

class Employment(db.Model):

    __tablename__ = "employments"
    
    researcher = db.relationship("Researcher", backref="education")
    researcher_id = db.Column(db.Integer, db.ForeignKey("researchers.user_id"),
                                                       primary_key=True)
    institution = XX
    location = XX
    years = AA
    
class Membership(db.Model):
    """The same as professional societies"""

    __tablename__ = "memberships"

    start_date  = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    society_name = XX
    membership_type = XX
    status = db.Column(db.Boolean)

class Award(db.Model):

    __tablename__ = "awards"

    year = db.Column(db.Integer)
    awarding_body = db.Column(db.String)
    details = db.Column(db.String)
    team_member_name = db.Column(db.String)

class FundingDiversification(db.Model):

    __tablename__ = "funding_diversification"

    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    amount = db.Column(db.Integer)
    funding_body = db.Column(db.String)
    funding_programme = db.Column(db.String)
    status = db.Column(db.Boolean)
    primary_attribution = db.Column(db.Integer, db.ForeignKey("calls.id"))

class TeamMember(db.Model):

    __tablename__ = "team_member"

    start_date = db.Column(db.DateTime)
    departure_date = db.Column(db.DateTime)
    name = db.Column(db.String)
    position = db.Column(db.String)
    primary_attribution = db.Column(db.Integer, db.ForeignKey("calls.id"))

class Impact(db.Model):

    __tablename__ = "impacts"

    title = db.Column(db.String)
    category = db.Column(db.String)
    primary_benneficiary = db.Column(db.String)
    primary_attribution = db.Column(db.Integer, db.ForeignKey("calls.id"))

class Publication(db.Model):

    __tablename__ = "publications"
    
    year = db.Column(db.Integer)

    original_article = XX
    review_article = XX
    conference_paper = XX
    book = XX
    technical_report = XX

    title = XX
    journal_name = XX

    is_published = db.Column(db.Boolean)
    in_press = db.Column(db.Boolean)
    DOI = XX
    primary_attribution = db.Column(db.Integer, db.ForeigmKey("calls.id"))

class Presentation(db.Model):

    __tablename__ = "presentations"

    year = db.Column(db.Integer)
    title = XX

    conference = XX
    invited_seminar = XX
    keynote = XX
    organizing_body = XX
    location = XX
    primary_attribution = db.Column(db.Integer, db.ForeignKey("calls.id"))

class AcademicCollaboration(db.Model):

    __tablename__ - "academic_collaborations"

    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    institution = XX
    institution_dept = XX
    location = XX
    collaborator_name = XX
    primary_goal = XX
    interaction_frequency = XX
    primary_attribution = db.Column(db.Integer, db.ForeignKey("calls.id"))

class NonAcademicCollaboration(db.Model):

    __tablename__ = "non_academic_collaborations"

    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    institution = XX
    institution_dept = XX
    location = XX
    collaborator_name = XX
    primary_goal = XX
    interaction_frequency = XX
    primary_attribution = db.Column(db.Integer, db.ForeignKey("calls.id"))

class Conference(db.Model):

    __tablename__ = "conferences"

    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    title = XX
    event_type = XX
    role = XX
    location = XX
    primary_attribution = db.Column(db.Integer, db.ForeignKey("calls.id"))

class CommunicationOverview(db.Model):
    
    __tablename__ = "communication_overview"

    year = db.Column(db.Integer)
    num_of_publication_lectures = db.Column(db.Integer)
    num_of_visits = db.Column(db.Integer)
    num_of_media_interactions = db.Column(db.Integer)

class SFIFundingRatio(db.Model):

    __tablename__ = "sfi_funding_ratios"

    year = db.Column(db.Integer)
    percentage_of_annual_spend = db.Column(db.Integer)

class EducationAndPublicEngagement(db.Model):

    __tablename__ = "education_and_public_engagement"

    project_name = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    activity_type = XX
    project_topic = XX
    target_graphical_area = XX
    primary_attribution = db.Column(db.Integer, db.ForeignKey("calls.id"))









class TeamMembers(db.Model):

    __tablename__ = 'team_members'
    
    member_id = db.Column(db.Integer, primary_key=True) #ID in team, not out of all members 
    start_date= db.Column(db.DateTime,nullable=True)  ##When inserting, datetime.date i think, not .datetime
    end_date = db.Column(db.DateTime,nullable=True)   ##
    name = db.Column(db.String(20),nullable=False)
    position = db.Column(db.String(80),nullable=False)
    primary_attribute = db.Column(db.String(12),nullable=True)
    researcher_id = db.Column(db.Integer, db.ForeignKey('researchers.user_id'), nullable = False)

    def __str__(self):
        return list(start_date, end_date, name, position, primary_attribute, researcher_id)

