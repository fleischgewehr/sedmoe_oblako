from secrets import token_urlsafe

from flask import (request, render_template, Blueprint, redirect,
                   url_for, send_from_directory)
from flask_login import current_user, logout_user, login_user
from flask_bcrypt import bcrypt
from werkzeug.utils import secure_filename

from evocloud.forms import FileForm, RegistrationForm, LoginForm
from evocloud.models import User, File
from evocloud import db, bcrypt
from evocloud.utils import round_date, time_left, allowed_file, get_extension
from evocloud.config import Config

routes = Blueprint('views', __name__)


@routes.route('/', methods=['GET', 'POST'])
def home():
    form = FileForm()
    if form.validate_on_submit():
        # save file to storage
        instance = request.files['file']
        name = secure_filename(form.filename.data +
                               get_extension(instance.filename))
        hash_name = str(token_urlsafe(8))
        if allowed_file(name):
            instance.save(Config.UPLOAD_FOLDER +
                          hash_name + get_extension(name))

            # save file into database
            exp = round_date(form.expiration.data)
            if current_user.is_authenticated:
                file = File(file=name, exp_date=exp, hash=hash_name,
                            owner_id=current_user.id)
            else:
                file = File(file=name, exp_date=exp, hash=hash_name,
                            owner_id=None)
            db.session.add(file)
            db.session.commit()
            return redirect(url_for('views.filepage', hash=file.hash))
    return render_template('home.html', title='Upload a file', form=form)


@routes.route('/file/<string:hash>')
def filepage(hash):
    file = File.query.filter_by(hash=hash).first()
    timer = time_left(file.exp_date)
    return render_template('filepage.html', file=file, alive=timer)


@routes.route('/download/<string:hash>')
def download(hash):
    file = File.query.filter_by(hash=hash).first()
    return send_from_directory(Config.UPLOAD_FOLDER,
                               file.hash + get_extension(file.file))


@routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RegistrationForm()
    if form.validate_on_submit() and not \
            User.query.filter_by(username=form.username.data).first():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('views.login'))
    return render_template('register.html', title='Register', form=form)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('views.home'))
    return render_template('login.html', title='Login', form=form)


@routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@routes.route('/user/<string:username>')
def profile(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    files = File.query.filter_by(owner=user).paginate(page=page, per_page=5)
    return render_template('profile.html', files=files, user=user)


@routes.errorhandler(403)
def page_not_found(e):
    return render_template('error.html'), 403


@routes.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


@routes.errorhandler(500)
def page_not_found(e):
    return render_template('error.html'), 500
