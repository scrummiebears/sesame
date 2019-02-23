from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, RadioField, IntegerField, TextAreaField, FormField, FieldList
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms.fields.html5 import DateTimeLocalField
from wtforms import validators, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets import DateInput, NumberInput

class EducationForm(FlaskForm):
    
    degree = StringField("Degree",description={"placeholder":"Degree"})
    field_of_study = StringField("Field of Study", description={"placeholder":"Field of study"})
    institution = StringField("Institution", description={"placeholder":"Institution"})
    location = StringField("Location", description={"placeholder":"Location"})
    degree_award_year = StringField("Year of Degree Award", description={"placeholder":"Year of degree award"})

class EmploymentForm(FlaskForm):

    institution = StringField("Institution/Company", description={"placeholder":"Institution/Company"})
    location = StringField("Location", description={"placeholder":"Location"})
    years = IntegerField("Years", widget=NumberInput(), description={"placeholder":"Years"})

class MembershipForm(FlaskForm):

    start_date = StringField("Start Date", widget=DateInput(), description={"placeholder":"Start date"})
    end_date = StringField("End Date", widget=DateInput(), description={"placeholder":"End date"})
    society_name = StringField("Society Name", description={"placeholder":"Society name"})
    membership_type = StringField("Membership Type", description={"placeholder":"Membership type"})

class AwardForm(FlaskForm):
    
    year = IntegerField("Year", description={"placeholder":"Year"})
    awarding_body = StringField("Awarding Body", description={"placeholder":"Awarding Body"})
    details = StringField("Details of Award", description={"placeholder":"details"})
    team_member_name = StringField("Team Member Name", description={"placeholder":"Team member name"}) 

