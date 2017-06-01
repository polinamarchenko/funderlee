from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.collections.models import Collection
from project.collections.forms import CollectionForm
from project import db

collections_blueprint = Blueprint(
  'collections',
  __name__,
  template_folder='templates'
)
