from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),Length(min=2,max=20)])
    password = PasswordField('Password',
                           validators=[DataRequired(),Length(min=6,max=30)])
    confirm_password = PasswordField('Confirm password',
                           validators=[DataRequired(),EqualTo('password'),Length(min=6,max=30)])
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    submit = SubmitField('Sign Up')
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose another one')
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose another one')
    
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    password = PasswordField('Password',
                           validators=[DataRequired(),Length(min=6,max=30)])
    submit = SubmitField('Login')
    remember = BooleanField('Remember me ?')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    picture = FileField('Update profile picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, please choose another one')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken, please choose another one')
            
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                           validators=[DataRequired(),Length(min=6,max=30)])
    confirm_password = PasswordField('Confirm password',
                           validators=[DataRequired(),EqualTo('password'),Length(min=6,max=30)])
    submit = SubmitField('Reset Password')
