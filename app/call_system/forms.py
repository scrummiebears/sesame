from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, RadioField, IntegerField, TextAreaField, FormField, FieldList
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms.fields.html5 import DateTimeLocalField
from wtforms import validators, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

class WordCount(object):
    def __init__(self, xmin=-1, xmax=-1, message=None):
        self.min = xmin
        self.max = xmax
        if not message:
            message = u'Field must be between %i and %i words long.' % (self.min, self.max)
        self.message = message

    def __call__(self, form, field):
        content = field.data.split()
        l = len(content)
        if l < self.min or (self.max != -1 and l > self.max):    
            raise ValidationError(self.message)

class CallForm(FlaskForm):

    information = TextAreaField("Information", [InputRequired()])
    target_group = TextAreaField("Target Group", [InputRequired()])
    proposal_template = TextAreaField("Proposal Template", [InputRequired()])
    deadline = DateTimeLocalField("Deadline", format='%Y-%m-%dT%H:%M')
    file = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDFs only!')])

class CollaboratorForm(FlaskForm):
    """Form to specify a collaborator for a propsoal

    Should be used in conjunction with ProposalForm
    """
    name = StringField()
    organization = StringField()
    email = StringField()
    
class ProposalForm(FlaskForm):
    """The form for a proposal in response to a call
    
    All fields are required.
    """
    
    title = StringField("Title", validators=[InputRequired()])
    duration = IntegerField("Duration", validators=[InputRequired()])
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
    nrp = SelectField("National Research Priority", choices=nrp_choices, validators=[InputRequired()])
    legal_remit = TextAreaField("Legal Remit", validators=[InputRequired()])
    ethical_issues = TextAreaField("Ethical Issues", validators=[InputRequired()])
    
    location = StringField("Country", validators=[InputRequired()])
    co_applicants = TextAreaField("Co-Applicants")
    collaborators = StringField("Collaborators")
    scientific_abstract = TextAreaField("Scientific Abstract", validators=[InputRequired(), WordCount(xmax=200)])
    lay_abstract = TextAreaField("Lay Abstract", validators=[InputRequired(), WordCount(xmax=100)])
    programme_documents = FileField("Programme Documents", validators=[InputRequired(message="You must provide programme documents in the form of a .pdf file")])

    agree = BooleanField("I agree", validators=[InputRequired(message="You must agree to the terms and conditions to submit a proposal")])