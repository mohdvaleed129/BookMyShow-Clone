from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FloatField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError, NumberRange
from models import User

class RegistrationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[
        DataRequired(message='Full name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    phone = StringField('Mobile Number', validators=[
        DataRequired(message='Phone number is required'),
        Regexp(r'^[0-9]{10,15}$', message='Please enter a valid phone number (10-15 digits)')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$',
    message='Password must contain at least one uppercase letter, one lowercase letter, and one digit'
)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords do not match')
    ])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please use a different email.')
    
    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('This phone number is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    remember = SelectField('Remember Me', choices=[('False', 'No'), ('True', 'Yes')], default='False')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    fullname = StringField('Full Name', validators=[
        DataRequired(message='Full name is required'),
        Length(min=2, max=100)
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    phone = StringField('Mobile Number', validators=[
        DataRequired(message='Phone number is required'),
        Regexp(r'^[0-9]{10,15}$', message='Please enter a valid phone number')
    ])
    submit = SubmitField('Update Profile')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message='Current password is required')
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$', 
               message='Password must contain at least one uppercase letter, one lowercase letter, and one digit')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your new password'),
        EqualTo('new_password', message='Passwords do not match')
    ])
    submit = SubmitField('Change Password')

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired(), Length(max=200)])
    genre = StringField('Genre', validators=[DataRequired(), Length(max=100)])
    language = SelectField('Language', choices=[
        ('English', 'English'), ('Hindi', 'Hindi'), ('Tamil', 'Tamil'), 
        ('Telugu', 'Telugu'), ('Malayalam', 'Malayalam'), ('Kannada', 'Kannada'),
        ('Marathi', 'Marathi'), ('Bengali', 'Bengali'), ('Punjabi', 'Punjabi'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    duration = StringField('Duration (e.g., 2h 30m)', validators=[DataRequired()])
    rating = FloatField('Rating (0-10)', validators=[DataRequired(), NumberRange(min=0, max=10)])
    description = TextAreaField('Description', validators=[DataRequired()])
    poster = StringField('Poster URL', default='')
    trailer = StringField('Trailer URL (YouTube embed)', default='')
    release_date = DateField('Release Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('now_showing', 'Now Showing'),
        ('coming_soon', 'Coming Soon')
    ], default='now_showing')
    submit = SubmitField('Save Movie')

class ShowForm(FlaskForm):
    movie_id = SelectField('Movie', coerce=int, validators=[DataRequired()])
    theatre = StringField('Theatre Name', validators=[DataRequired(), Length(max=200)])
    show_date = DateField('Show Date', validators=[DataRequired()])
    show_time = TimeField('Show Time', validators=[DataRequired()])
    screen = StringField('Screen', default='Screen 1', validators=[Length(max=50)])
    submit = SubmitField('Save Show')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')