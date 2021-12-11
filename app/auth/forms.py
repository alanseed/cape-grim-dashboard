# WTF forms to manage users 

# Based on the Flask Mega-Tutorial 
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.db import get_db

# TO DO - Use the User class to manage user authentication 
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        print(str(username))
        user = get_db()["users"]
        myquery = {"name":str(username)}
        mydoc = user.find_one(myquery)
        if mydoc is not None: 
            raise ValidationError('Please use a different username.')
            
    def validate_email(self, email):
        print(str(email))
        user = get_db()["users"]
        myquery = {"email":str(email)}
        mydoc = user.find_one(myquery)
        if mydoc is not None: 
            raise ValidationError('Please use a different email address.')
            
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In') 
