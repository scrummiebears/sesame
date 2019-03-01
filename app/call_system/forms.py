from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, RadioField, IntegerField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired
from wtforms.fields.html5 import DateTimeLocalField
from wtforms import validators
from flask_wtf.file import FileField, FileAllowed, FileRequired

# class CountrySelectField(SelectField):
#     def __init__(self, *args, **kwargs):
#         super(CountrySelectField, self).__init__(*args, **kwargs)
#         self.choices = [(country.alpha_2, country.name) for country in pycountry.countries]

class CallForm(FlaskForm):
    """Form for Call for Proposals

    This form has been updated to reflect call information in Briefing 4
    """

    information = TextAreaField("Information", [InputRequired()])
    target_group = TextAreaField("Target Group", [InputRequired()])
    proposal_template = TextAreaField("Proposal Template", [InputRequired()])
    deadline = DateTimeLocalField("Deadline", format='%Y-%m-%dT%H:%M')

    eligibility_criteria = StringField("Eligibility Criteria", [InputRequired()])
    duration_of_award = StringField("Duration of Award", [InputRequired()])
    reporting_guidelines = StringField("Reporting Guidelines", [InputRequired()])
    expected_start_date = StringField("Expected Start Date", [InputRequired()]) # String Field because can be a date range

    file = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDFs only!')])

class ProposalForm(FlaskForm):
    """The form for a proposal in response to a call
    
    All fields are required
    """
    
    title = StringField("Title")
    duration = IntegerField("Duration")
    nrp_choices = [("A", "Priority Area A - Future Networks & Communications"),
                   ("B", "Priority Area B - Data analytics, Management, Security & Privacy"),
                   ("C", "Priority Area C - Digital Platforms, Content & Applications"), 
                   ("D", "Priority Area D - Conected Health and Independant Living"), 
                   ("E", "Priority Area E - Medical Devices"), 
                   ("F", "Priority Area F - Diagnostics"), 
                   ("G", "Priority Area G - Therapeutics: Syntesis, Formulation, Processing, and Drug Delivery"),
                   ("H", "Priority Area H - Food for Health"), 
                   ("I", "Priority Area I - Sustainable Food Production and Processing"), 
                   ("J", "Priority Area J - Marine Renewable Energy"), 
                   ("K", "Priority Area K - Smart Grids & Smart Cities"), 
                   ("L", "Priority Area L - Manufacturing Competitvness"), 
                   ("M", "Priority Area M - Processing Technologies and Novel Materials"), 
                   ("N", "Priority Area N - Innovation in Services and Business Processes"), 
                   ("O", "Software"),
                   ("P", "Other")]
    nrp = SelectField("National Research Priority", choices=nrp_choices)
    legal_remit = TextAreaField("Legal Remit")
    ethical_issues = TextAreaField("Ethical Issues")
    
    location = StringField("Country")
    co_applicants = TextAreaField("Co-Applicants")
    collaborators = TextAreaField("Collaborators")
    scientific_abstact = TextAreaField("Scientific Abstract")
    lay_abstract = TextAreaField("Lay Abstract")
    programme_documents = FileField("Programme Documents")

    agree = BooleanField("I agree")    