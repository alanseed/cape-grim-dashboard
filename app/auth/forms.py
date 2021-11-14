# Based on the Flask Mega-Tutorial 
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.db import get_db 

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        db = get_db()
        error = None
        sql = f"SELECT * FROM user WHERE username = '{username}'" 
        user = db.execute(sql).fetchone()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        db = get_db()
        error = None
        sql = f"SELECT * FROM user WHERE email = '{email}'"
        user = db.execute(sql).fetchone()

        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')