from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.datetime import DateField
from wtforms.widgets.core import DateInput

class DateForm(FlaskForm):
    date = DateField(label='Chart Date',validators=[DateInput()])
    submit=SubmitField('Submit')    