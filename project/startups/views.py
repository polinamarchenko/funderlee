from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.startups.models import Startup
from project import db

startups_blueprint = Blueprint(
  'startups',
  __name__,
  template_folder='templates'
)
