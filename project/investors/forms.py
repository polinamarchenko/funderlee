from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length

class InvestorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    url = StringField('website', validators=[DataRequired(), Email()])
    country = StringField('location', validators=[Length(min=6)])
