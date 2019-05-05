from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Email, NumberRange
from wtforms import (StringField, SubmitField, IntegerField,
                     FileField, BooleanField, PasswordField)


class FileForm(FlaskForm):
    filename = StringField('Filename', validators=[DataRequired()])
    file = FileField('File', validators=[DataRequired()])
    expiration = IntegerField(
        'Hours to expire', validators=[
            DataRequired(),
            NumberRange(min=1, message='Must be greater than 1')
        ])
    submit = SubmitField('Upload')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Sign up')
