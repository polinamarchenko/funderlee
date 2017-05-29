from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.users.models import User
from project.users.forms import UserForm
from project import db
from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
  'users',
  __name__,
  template_folder='templates'
)

@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()
    return render_template('users/signup.html', form=form)
