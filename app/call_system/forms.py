from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired
from wtforms.fields.html5 import DateTimeLocalField
from wtforms import validators
class CallForm(FlaskForm):

    information = TextAreaField("Information", [InputRequired()])
    target_group = TextAreaField("Target Group", [InputRequired()])
    proposal_template = TextAreaField("Proposal Template", [InputRequired()])
    deadline = DateTimeLocalField("Deadline", format='%Y-%m-%dT%H:%M')
    file = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDFs only!')])
