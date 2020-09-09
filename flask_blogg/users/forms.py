
from flask_wtf import FlaskForm
from wtforms import StringField ,  PasswordField , BooleanField , SubmitField
from wtforms.validators import DataRequired , ValidationError , Length , Email , EqualTo
from flask_login import current_user
from flask_blogg.models import User
from wtforms.widgets import TextArea


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign UP")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'The username is already taken. Please try with a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'The email is already taken. Please try with a different one')


class UpdateForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = StringField('About Me', widget=TextArea())
    submit = SubmitField("Sign UP")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'The username is already taken. Please try with a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user and user.email != current_user.email:
                raise ValidationError(
                    'The email is already taken. Please try with a different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login !')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset !')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with that email , you must register first")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password!')
