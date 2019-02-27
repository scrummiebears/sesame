from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")

class RegistrationForm(FlaskForm):
    email = StringField("Email", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])

    first_name = StringField("First name", [InputRequired()])
    last_name = StringField("Last name", [InputRequired()])
    job_title = StringField("Job title", [InputRequired()])
    prefix = StringField("Prefix", [InputRequired()])

    suffix = StringField("Suffix")
    phone = IntegerField("Phone")
    phone_ext = IntegerField("Phone Extension")
    orcid = StringField("Orcid")

class TeamForm(FlaskForm):
    start_date = DateField('Start date',validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    end_date =  DateField('Departure Date',validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    name = StringField('Name',
                       validators=[InputRequired(),Length(min=3,max=20)])
    position = StringField('Position',
                       validators=[InputRequired(),Length(max=80)])
    grant_number = IntegerField('Primary Attribute',validators=[InputRequired()]
