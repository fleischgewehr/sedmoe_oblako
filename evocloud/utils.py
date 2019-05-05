from datetime import timedelta, datetime
import os

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


def round_date(delta):
    exp = datetime.now() + timedelta(hours=delta)

    rounded = exp.replace(minute=0, second=0, microsecond=0)
    half = exp.replace(minute=30, second=0, microsecond=0)

    return rounded if exp < half else rounded + timedelta(hours=1)


def time_left(dt):
    return str(dt - datetime.now()).split('.')[0]


def next_hour():
    return datetime.now().replace(
        minute=0, second=0, microsecond=0) + timedelta(hours=1)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_extension(filename):
    return os.path.splitext(filename)[1]
