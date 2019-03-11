from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField, SelectField, RadioField, IntegerField, TextAreaField, FormField, FieldList
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms.fields.html5 import DateTimeLocalField
from wtforms import validators, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets.html5 import DateInput, NumberInput

class ReviewerForm(FlaskForm):
    comments = TextAreaField("Comments")
    action = SelectField("Action", choices=[("Approve", "Approve"), ("Reject","Reject"),( "Save", "Save")])

class ReviewerLoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")