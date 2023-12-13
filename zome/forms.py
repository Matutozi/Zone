#!/usr/bin/env python3
"""Module that implements the forms feature of the application
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, TextAreaField, FloatField, IntegerField
from flask_login import current_user
from wtforms.validators import (
        DataRequired, Length, Email, EqualTo, ValidationError
        )
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from zome.models import User


class RegistrationForm(FlaskForm):
    """Class that handles the registration task for new users"""
    username = StringField(
            "Username",
            validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField(
        "Surname",
        validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField(
        "First_name",
        validators=[DataRequired(), Length(min=2, max=20)])
    other_name = StringField(
        "Other_name",
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
            "Confirm Password",
            validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """to validate the uername provided by user against database"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken, choose another one")

    def validate_email(self, email):
        """module that validates email provded by new user against database"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken, choose another one")


class Login(FlaskForm):
    """class that handles the login task of user"""
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    Submit = SubmitField("Login")


class UpdateForm(FlaskForm):
    """class that updates information"""
    username =  StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class ListingForm(FlaskForm):
    """module that stores listing data for storage in the database"""
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    size = FloatField('Size', validators=[DataRequired()])
    image = FileField('Add an Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Listing')

class LandListingForm(ListingForm):
    """module that stores land listing data and inherits from listing form"""
    land_specific_field = FloatField('Land Specific Field', validators=[DataRequired()])
    submit_land = SubmitField('Add Land Listing')

class HouseListingForm(ListingForm):
    """module that stores house listing data and inherits from listing form"""
    number_rooms = IntegerField('Number of Rooms', validators=[DataRequired()])
    number_bathrooms = IntegerField('Number of Bathrooms', validators=[DataRequired()])
    house_specific_field = StringField('House Specific Field', validators=[DataRequired()])
    submit_house = SubmitField('Add House Listing')