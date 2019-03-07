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
    proposal_template = FileField("Proposal Template", [InputRequired()])
    deadline = StringField("Deadline")

    eligibility_criteria = TextAreaField("Eligibility Criteria", [InputRequired()])
    duration_of_award = StringField("Duration of Award", [InputRequired()])
    reporting_guidelines = TextAreaField("Reporting Guidelines", [InputRequired()])
    expected_start_date = StringField("Expected Start Date", [InputRequired()]) # String Field because can be a date range

    file = FileField('image', validators=[FileAllowed(['pdf'], 'PDFs only!')])

class ProposalForm(FlaskForm):
    """The form for a proposal in response to a call

    All fields are required
    """

    title = StringField("Title")
    duration = IntegerField("Duration")
    nrp_choices = [("Priority Area A - Future Networks & Communications", "Priority Area A - Future Networks & Communications"),
                   ("Priority Area B - Data analytics, Management, Security & Privacy", "Priority Area B - Data analytics, Management, Security & Privacy"),
                   ("Priority Area C - Digital Platforms, Content & Applications", "Priority Area C - Digital Platforms, Content & Applications"),
                   ("Priority Area D - Conected Health and Independant Living", "Priority Area D - Conected Health and Independant Living"),
                   ("Priority Area E - Medical Devices", "Priority Area E - Medical Devices"),
                   ("Priority Area F - Diagnostics", "Priority Area F - Diagnostics"),
                   ("Priority Area G - Therapeutics: Syntesis, Formulation, Processing, and Drug Delivery", "Priority Area G - Therapeutics: Syntesis, Formulation, Processing, and Drug Delivery"),
                   ("Priority Area H - Food for Health", "Priority Area H - Food for Health"),
                   ("Priority Area I - Sustainable Food Production and Processing", "Priority Area I - Sustainable Food Production and Processing"),
                   ("Priority Area J - Marine Renewable Energy", "Priority Area J - Marine Renewable Energy"),
                   ("Priority Area K - Smart Grids & Smart Cities", "Priority Area K - Smart Grids & Smart Cities"),
                   ("Priority Area L - Manufacturing Competitvness", "Priority Area L - Manufacturing Competitvness"),
                   ("Priority Area M - Processing Technologies and Novel Materials", "Priority Area M - Processing Technologies and Novel Materials"),
                   ("Priority Area N - Innovation in Services and Business Processes", "Priority Area N - Innovation in Services and Business Processes"),
                   ("Software", "Software"),
                   ("Other", "Other")]
    nrp = SelectField("National Research Priority", choices=nrp_choices)
    legal_remit = TextAreaField("Legal Remit")
    ethical_issues = TextAreaField("Ethical Issues")

    location = StringField("Country")
    co_applicants = TextAreaField("Co-Applicants")
    collaborators = TextAreaField("Collaborators")
    scientific_abstract = TextAreaField("Scientific Abstract")
    lay_abstract = TextAreaField("Lay Abstract")
    programme_documents = FileField("Programme Documents")

    agree = BooleanField("I agree")
