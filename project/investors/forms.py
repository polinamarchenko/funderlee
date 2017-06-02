from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length

class InvestorForm(FlaskForm):
    investor = StringField('investor', validators=[DataRequired()])
