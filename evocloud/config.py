from os.path import join, dirname, realpath
from os import environ


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024
