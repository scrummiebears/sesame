from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, RadioField, IntegerField, TextAreaField, FormField, FieldList
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms.fields.html5 import DateTimeLocalField
from wtforms import validators, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets.html5 import DateInput, NumberInput

class EducationForm(FlaskForm):
    
    degree = StringField("Degree",description={"placeholder":"Degree"})
    field_of_study = StringField("Field of Study", description={"placeholder":"Field of study"})
    institution = StringField("Institution", description={"placeholder":"Institution"})
    location = StringField("Location", description={"placeholder":"Location"})
    degree_award_year = StringField("Year of Degree Award", description={"placeholder":"Year of degree award"})

class EmploymentForm(FlaskForm):

    institution = StringField("Institution/Company", description={"placeholder":"Institution/Company"})
    location = StringField("Location", description={"placeholder":"Location"})
    years = IntegerField("Years", description={"placeholder":"Years"})

class MembershipForm(FlaskForm):

    start_date = StringField("Start Date", description={"placeholder":"Start date"})
    end_date = StringField("End Date", description={"placeholder":"End date"})
    society_name = StringField("Society Name", description={"placeholder":"Society name"})
    membership_type = StringField("Membership Type", description={"placeholder":"Membership type"})

class AwardForm(FlaskForm):
    
    year = IntegerField("Year", description={"placeholder":"Year"})
    awarding_body = StringField("Awarding Body", description={"placeholder":"Awarding Body"})
    details = StringField("Details of Award", description={"placeholder":"details"})
    team_member_name = StringField("Team Member Name", description={"placeholder":"Team member name"}) 

class FundingDiversificationForm(FlaskForm):

    start_date = StringField("Start Date", description={"placeholder":"Start date"})
    end_date = StringField("End Date", description={"placeholder":"End date"})
    amount = IntegerField("Amount", widget=NumberInput(), description={"placeholder": "Amount"})
    funding_body = StringField("Funding Body", description={"placeholder": "Funding body"})
    funding_programme = StringField("Funding Programme", description={"placeholder": "Funding programme"})
    primary_attribution = IntegerField("Primary Attribution", description={"placeholder": "Primary attribution"})

class TeamMemberForm(FlaskForm):

    start_date = StringField("Start Date", description={"placeholder":"Start date"})
    departure_date = StringField("Departure Date", description={"placeholder":"Departure date"})
    name = StringField("Name", description={"placeholder": "Name"})
    position = StringField("Position", description={"placeholder": "Position"})
    primary_attribution = IntegerField("Primary Attribution", description={"placeholder": "Primary attribution"})

class ImpactForm(FlaskForm):

    title = StringField("Title", description={"placeholder": "Title"})
    category = StringField("Category", description={"placeholder": "Category"})
    primary_beneficiary = StringField("Primary Beneficiary", description={"placeholder": "Primary Benneficiary"})
    primary_attribution = IntegerField("Primary Attribution", description={"placeholder": "Primary attribution"})

class InnovationForm(FlaskForm):
    
    year = IntegerField("Year", description={"placeholder": "Year"})
    innovation_type = StringField("Innovation Type", description={"placeholder": "Innovation type"})
    title = StringField("Title", description={"placeholder": "Title"})
    primary_attribution = IntegerField("Primary Attribution", description={"placeholder": "Primary attribution"})

class PublicationForm(FlaskForm):

    year = IntegerField("Year", description={"placeholder": "Year"})

    original_article = StringField("Original Aritcle", description={"placeholder": "Original article"})
    review_article = StringField("Review Article", description={"placeholder": "Reveiw article"})
    conference_paper = StringField("Conference Paper", description={"placeholder": "Conference paper"})
    book = StringField("Book", description={"placeholder": "Book"})
    technical_report = StringField("Technical Report", description={"placeholder": "Technical report"})

    title = StringField("Title", description={"placeholder": "Title"})
    journal_name = StringField("Journal Name", description={"placeholder": "Journal name"})

    DOI = StringField()
    primary_attribution = IntegerField("Primary Attribution", description={"placeholder": "Primary attribution"})
    is_published = BooleanField("Is Published")
    in_press = BooleanField("In Press")

class PresentationForm(FlaskForm):

    year = IntegerField("Year", description={"placeholder": "Year"})
    title = StringField("Title", description={"placeholder": "Title"})
    conference = StringField("Journal/Conference Name", description={"placeholder": "Conference"})
    invited_seminar = StringField("Invited Seminar", description={"placeholder": "Invited seminar"})
    keynote = StringField("Keynote", description={"placeholder": "Keynote"})
    organizing_body = StringField("Organizing Body", description={"placeholder": "Organizing Body"})
    location = StringField("Location", description={"placeholder": "Location"})
    primary_attribution = IntegerField("Primary Attribution", description={"placeholder": "Primary attribution"})

class AcademicCollaborationForm(FlaskForm):

    start_date = StringField("Start Date", widget=DateInput())
    end_date = StringField("Start Date", widget=DateInput())
    institution = StringField("Institution", description={"placeholder": "Institution"})
    location = StringField("Location", description={"placeholder": "Location"})
    collaborator_name = StringField("Collaborator Name", description={"placeholder": "Collaborator name"})
    primary_goal = StringField("Primary Goal", description={"placeholder": "Primary goal"})
    interaction_frequency = IntegerField("Interaction Frequency", validators=[NumberRange(min=0, max=100)])
    primary_attribution = IntegerField("Primary Attribution", description={"placeholder": "Primary attribution"})

class NonAcademicCollaborationForm(FlaskForm):

    start_date = StringField("Start Date", widget=DateInput())
    end_date = StringField("Start Date", widget=DateInput())
    institution = StringField("Institution", description={"placeholder": "Institution"})
    location = StringField("Location", description={"placeholder": "Location"})
    collaborator_name = StringField("Collaborator Name", description={"placeholder": "Collaborator name"})
    primary_goal = StringField("Primary Goal", description={"placeholder": "Primary goal"})
    interaction_frequency = IntegerField("Interaction Frequency", validators=[NumberRange(min=0, max=100)], description={"placeholder": "Interaction frequency"})
    primary_attribution = IntegerField("Primary Attribution", description={"placeholder": "Primary attribution"})

class ConferenceForm(FlaskForm):

    start_date = StringField("Start Date")
    end_date = StringField("Start Date")
    title = StringField("Title", description={"placeholder": "Title"})
    event_type = StringField("Event Type", description={"placeholder": "Event type"})
    role = StringField("Role", description={"placeholder": "Role"})
    location = StringField("Location", description={"placeholder": "Location"})
    primary_attribution = IntegerField("Primary Attribution", description={"placeholder": "Primary attribution"})

class CommunicationOverviewForm(FlaskForm):

    year = IntegerField("Year", description={"placeholder": "Year"})
    num_of_public_lectures = IntegerField("Number of Public Lectures/Demonstrations", widget=NumberInput())
    num_of_visits = IntegerField("Number of Visits", widget=NumberInput())
    num_of_media_interactions = IntegerField("Number of Media Interactions", widget=NumberInput())

class SFIFundingRatioForm(FlaskForm):

    year = IntegerField("Year")
    percentage_of_annual_spend = IntegerField("Percentage of Annual Spend", widget=NumberInput(), validators=[NumberRange(min=0, max=100)])

class EducationAndPublicEngagementForm(FlaskForm):

    project_name = StringField("Project name", description={"placeholder": "Project name"})
    start_date = StringField("Start Date", widget=DateInput())
    end_date = StringField("Start Date", widget=DateInput())
    activity_type = StringField("Activity Type", description={"placeholder": "Activity type"})
    project_topic = StringField("Project Type", description={"placeholder": "Project topic"})
    target_graphical_area = StringField("Target Graphical Area", description={"placeholder": "Target graphical area"})
    primary_attribution = IntegerField("Primary Attribution", description={"placeholder": "Primary attribution"})
