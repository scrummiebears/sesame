from flask_sqlalchemy import SQLAlchemy

from app import db
from app.auth.models import User

class Researcher(db.Model):

    __tablename__ = "researchers"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    prefix = db.Column(db.String, nullable=False)

    suffix = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    phone_ext = db.Column(db.String, nullable=True)
    orcid = db.Column(db.String, nullable=True)
    
    #researcher = db.relationship("Researcher", backref="grant_number") ##Relationship between grant and researcher.
    primary_attribute = db.Column(db.String(12), nullable=True) #db.ForeignKey("grants.number") ##
    
    team = db.relationship("TeamMembers", backref="researcher_id", lazy=True)

class Education(db.Model):

    __tablename__ = "education"

    researcher_id = db.Column(db.Integer, db.ForeignKey("researchers.user_id"),
                                                       primary_key=True)
    degree = db.Column(db.String, nullable=True)
    field_of_study = db.Column(db.String, nullable=True)
    institution = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    degree_award_year = db.Column(db.String, nullable=True)
    
class TeamMembers(db.Model):

    __tablename__ = 'team_members'
    
    member_id = db.Column(db.Integer, primary_key=True) #ID in team, not out of all members 
    start_date= db.Column(db.DateTime,nullable=False)  ##When inserting, datetime.date i think, not .datetime
    end_date = db.Column(db.DateTime,nullable=False)   ##
    name = db.Column(db.String(20),nullable=False)
    position = db.Column(db.String(80),nullable=False)
    primary_attribute = db.Column(db.String(12),nullable=False)
    reseacher_id = db.Column(db.Integer, db.ForeignKey('teams.researcher'), nullable = True) #Change to false when grant table is made.
    

    def __init__(self, start_date, end_date, name, position, primary_attribute):
        self.start_date = start_date
        self.end_date = end_date
        self.name = name
        self.position = position
        self.primary_attribute = primary_attribute

