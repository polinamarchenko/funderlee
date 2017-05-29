from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  fullname = StringField('username', validators=[DataRequired()])
  email = StringField('email', validators=[DataRequired(), Email()])
  password = PasswordField('password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])
