from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignupForm(Form):

    firstName = StringField('First Name', validators=[DataRequired("Please enter your first name.")],render_kw={"placeholder":"John"})
    lastName = StringField('Last Name', validators=[DataRequired("Please enter your last name.")],render_kw={"placeholder":"Johnson"})
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter a valid email address.")],
    					render_kw={"placeholder":"johnson@saveory.com"})
    password = PasswordField('Password', validators=[DataRequired("Please enter your password."), 
    												Length(min=8, message="Passwords must be 6 characters or more.")])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired("Please repeat your password"), 
    																EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Sign up')

    
        

class SigninForm(Form):
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter a valid email address.")],
    					render_kw={"placeholder":"johnson@saveory.com"})
    password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
    submit = SubmitField('Sign in')

class ProfileForm(Form):
    pass
    