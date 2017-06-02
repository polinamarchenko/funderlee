from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.users.models import User
from project.investors.models import Investor
from project.startups.models import Startup
from project.users.forms import UserForm, LoginForm, EditForm, PasswordForm
from project.collections.forms import CollectionForm
from project.investors.forms import InvestorForm
from project import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps

users_blueprint = Blueprint(
  'users',
  __name__,
  template_folder='templates'
)

def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('id') != current_user.id:
            flash({'text': "Not Authorized", 'status': 'danger'})
            return redirect(url_for('root'))
        return fn(*args, **kwargs)
    return wrapper

@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()
    if request.method == "POST":
        if form.validate():
            try:
                new_user = User(
                  username=form.username.data,
                  email=form.email.data,
                  password=form.password.data
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
            except IntegrityError as e:
                flash({'text': "Username is taken", 'status': 'danger'})
                return render_template('users/signup.html', form=form)
        return redirect(url_for('root'))
    return render_template('users/signup.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            found_user = User.query.filter_by(username = form.username.data).first()
            if found_user:
                is_authenticated = bcrypt.check_password_hash(found_user.password, form.password.data)
                if is_authenticated:
                    login_user(found_user)
                    flash({'text': "Hello, {}!".format(found_user.username), 'status': 'success'})
                    return redirect(url_for('root'))
            flash({'text': "Wrong credentials", 'status': 'danger'})
            return render_template('users/login.html', form=form)
    return render_template('users/login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
  logout_user()
  flash({ 'text': "You have successfully logged out.", 'status': 'success' })
  return redirect(url_for('users.login'))

@users_blueprint.route('/<int:id>', methods=['GET', 'PATCH'])
@login_required
@ensure_correct_user
def show(id):
    found_user = User.query.get(id)
    if request.method == 'GET':
        form = EditForm(obj=found_user)
        return render_template('users/show.html', user=found_user, form=form)

    if request.method == b'PATCH':
        if request.form.get('username', None) is not None:
            form = EditForm(request.form)
            if form.validate():
                found_user.username = form.username.data
                found_user.email = form.email.data
                is_authenticated = bcrypt.check_password_hash(found_user.password, form.password.data)
                if is_authenticated:
                    db.session.add(found_user)
                    db.session.commit()
                    return redirect(url_for('root'))
            return render_template('users/show.html', user=found_user, form=form)
        else:
            form2 = PasswordForm(request.form)
            if form2.validate():
                if bcrypt.check_password_hash(found_user.password,form2.current.data):
                    found_user.new_password = bcrypt.generate_password_hash(form2.new_password.data).decode('UTF-8')
                    db.session.add(found_user)
                    db.session.commit()
                    flash('You have succesfully changed your password')
                    return redirect(url_for('root'))
                flash('Please provide the right password')
                return render_template('users/password.html', form=form2, user=found_user)
            return render_template('users/password.html', form=form2, user=found_user)

@users_blueprint.route('/<int:id>/password')
def password(id):
    user = User.query.get(id)
    form = PasswordForm(request.form)
    return render_template('users/password.html', form=form, user=user)

@users_blueprint.route('/<int:id>/collection', methods=['GET', 'POST'])
def collection(id):
    user = User.query.get(id)
    if request.method == 'POST':
        form = InvestorForm(request.form)
        found_investor = Investor.query.filter_by(name=form.investor.data).first()
        current_user.investors.remove(found_investor)
        db.session.commit()
        return render_template('users/collection.html', form=form)
    return render_template('users/collection.html', user=user)


@users_blueprint.route('/foodtech', methods=['GET', 'POST'])
@login_required
def foodtech():
    investors = Investor.query.all()
    startups = Startup.query.all()
    if request.method == 'POST':
        if request.form.get('investor', None) is not None:
            form = InvestorForm(request.form)
            found_investor = Investor.query.filter_by(name=form.investor.data).first()
            if not found_investor in current_user.investors:
                current_user.investors.append(found_investor)
                db.session.add(found_investor)
                db.session.commit()
            else:
                current_user.investors.remove(found_investor)
                db.session.commit()
            return render_template('users/foodtech.html', investors=investors, startups=startups, form=form)
        else:
            form2 = CollectionForm(request.form)
            if form2.validate():
                collection = Collection(name=form2.name.data, user_id=current_user.id)
                db.session.add(collection)
                db.session.commit()
                flash('You have created a new collection')
                return render_template('users/foodtech.html', investors=investors, startups=startups, form=form2)
            flash('Collection name cannot be empty')
            return render_template('users/new.html', form=form2)
    return render_template('users/foodtech.html', investors=investors, startups=startups)


@users_blueprint.route('/ai', methods=['GET', 'POST'])
@login_required
def ai():
    investors = Investor.query.all()
    startups = Startup.query.all()
    if request.method == 'POST':
        if request.form.get('investor', None) is not None:
            form = InvestorForm(request.form)
            found_investor = Investor.query.filter_by(name=form.investor.data).first()
            if not found_investor in current_user.investors:
                current_user.investors.append(found_investor)
                db.session.add(found_investor)
                db.session.commit()
            else:
                current_user.investors.remove(found_investor)
                db.session.commit()
            return render_template('users/ai.html', investors=investors, startups=startups, form=form)
        else:
            form2 = CollectionForm(request.form)
            if form2.validate():
                collection = Collection(name=form2.name.data, user_id=current_user.id)
                db.session.add(collection)
                db.session.commit()
                flash('You have created a new collection')
                return render_template('users/ai.html', investors=investors, startups=startups, form=form2)
            flash('Collection name cannot be empty')
            return render_template('users/new.html', form=form2)
    return render_template('users/ai.html', investors=investors, startups=startups)

@users_blueprint.route('/fashiontech', methods=['GET', 'POST'])
@login_required
def fashion():
    investors = Investor.query.all()
    startups = Startup.query.all()
    if request.method == 'POST':
        if request.form.get('investor', None) is not None:
            form = InvestorForm(request.form)
            found_investor = Investor.query.filter_by(name=form.investor.data).first()
            if not found_investor in current_user.investors:
                current_user.investors.append(found_investor)
                db.session.add(found_investor)
                db.session.commit()
            else:
                current_user.investors.remove(found_investor)
                db.session.commit()
            return render_template('users/fashiontech.html', investors=investors, startups=startups, form=form)
        else:
            form2 = CollectionForm(request.form)
            if form2.validate():
                collection = Collection(name=form2.name.data, user_id=current_user.id)
                db.session.add(collection)
                db.session.commit()
                flash('You have created a new collection')
                return render_template('users/fashiontech.html', investors=investors, startups=startups, form=form2)
            flash('Collection name cannot be empty')
            return render_template('users/new.html', form=form2)
    return render_template('users/fashiontech.html', investors=investors, startups=startups)

@users_blueprint.route('/biotech', methods=['GET', 'POST'])
@login_required
def biotech():
    investors = Investor.query.all()
    startups = Startup.query.all()
    if request.method == 'POST':
        if request.form.get('investor', None) is not None:
            form = InvestorForm(request.form)
            found_investor = Investor.query.filter_by(name=form.investor.data).first()
            if not found_investor in current_user.investors:
                current_user.investors.append(found_investor)
                db.session.add(found_investor)
                db.session.commit()
            else:
                current_user.investors.remove(found_investor)
                db.session.commit()
            return render_template('users/biotech.html', investors=investors, startups=startups, form=form)
        else:
            form2 = CollectionForm(request.form)
            if form2.validate():
                collection = Collection(name=form2.name.data, user_id=current_user.id)
                db.session.add(collection)
                db.session.commit()
                flash('You have created a new collection')
                return render_template('users/biotech.html', investors=investors, startups=startups, form=form2)
            flash('Collection name cannot be empty')
            return render_template('users/new.html', form=form2)
    return render_template('users/biotech.html', investors=investors, startups=startups)

@users_blueprint.route('/fitnesstech', methods=['GET', 'POST'])
@login_required
def fitnesstech():
    per_page = 20
    investors = Investor.query.order_by('name').paginate(1,per_page,error_out=False)
    startups = Startup.query.all()
    if request.method == 'POST':
        if request.form.get('investor', None) is not None:
            form = InvestorForm(request.form)
            found_investor = Investor.query.filter_by(name=form.investor.data).first()
            if not found_investor in current_user.investors:
                current_user.investors.append(found_investor)
                db.session.add(found_investor)
                db.session.commit()
            else:
                current_user.investors.remove(found_investor)
                db.session.commit()
            return render_template('users/fitnesstech.html', investors=investors, startups=startups, form=form)
        else:
            form2 = CollectionForm(request.form)
            if form2.validate():
                collection = Collection(name=form2.name.data, user_id=current_user.id)
                db.session.add(collection)
                db.session.commit()
                flash('You have created a new collection')
                return render_template('users/fitnesstech.html', investors=investors, startups=startups, form=form2)
            flash('Collection name cannot be empty')
            return render_template('users/new.html', form=form2)
    return render_template('users/fitnesstech.html', investors=investors, startups=startups)

@users_blueprint.route('/fitnesstech/<int:page>')
def view(page=1):
    per_page = 20
    investors = Investor.query.order_by('name').paginate(page,per_page,error_out=False)
    return render_template('users/fitnesstech.html',investors=investors)

@users_blueprint.route('/agtech', methods=['GET', 'POST'])
@login_required
def agtech():
    per_page = 50
    page = int(request.args.get("page", -1))
    if page < 0:
        page = 1
    investors = Investor.query.order_by('name').paginate(page,120,error_out=False)
    startups = Startup.query.order_by('name').paginate(page,per_page,error_out=False)
    if request.method == 'POST':
        if request.form.get('investor', None) is not None:
            form = InvestorForm(request.form)
            found_investor = Investor.query.filter_by(name=form.investor.data).first()
            if not found_investor in current_user.investors:
                current_user.investors.append(found_investor)
                db.session.add(found_investor)
                db.session.commit()
            else:
                current_user.investors.remove(found_investor)
                db.session.commit()
            return redirect(url_for('users.agtech', page=page))
    return render_template('users/agtech.html', investors=investors, startups=startups)

@users_blueprint.route('/agtech/<int:page>')
def agt(page=1):
    per_page = 20
    investors = Investor.query.order_by('name').paginate(page,120,error_out=False)
    startups = Startup.query.order_by('name').paginate(page,per_page,error_out=False)
    return render_template('users/agtech.html',investors=investors, startups=startups)
