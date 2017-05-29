from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.investors.models import Investor
from project import db
from sqlalchemy.exc import IntegrityError

investors_blueprint = Blueprint(
  'investors',
  __name__,
  template_folder='templates'
)
