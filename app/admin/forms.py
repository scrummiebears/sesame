from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField

class NewAdminForm(FlaskForm):

    email = StringField("Email")
    password = PasswordField("Password")

    first_name = StringField("First Name")
    last_name = StringField("Last name")

class AssignReviewersForm(FlaskForm):
    emails = StringField("emails")