from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class Usersignupform(FlaskForm):
    name = StringField(label='Name', validators=[Length(min=2, max=100)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirmpassword = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign Up')

class Userloginform(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=30)])
    submit = SubmitField(label='Login')

class Jobform(FlaskForm):
    data = FileField(label='Upload CV', validators=[FileAllowed(['pdf', 'doc'])])
    submit = SubmitField(label='Upload')

class Jobforms(FlaskForm):
    compname = StringField(label='Enter company name', validators=[DataRequired(), Length(min=2, max=100)])
    location = StringField(label='Enter country or postal code of job', validators=[DataRequired(), Length(min=2, max=100)])
    sector = RadioField(label='Sector', choices=[('IT', 'IT'), ('Business', 'Business'), ('Any', 'Any')], default='IT')
    service_period = RadioField(label='Service Period', choices=[('12 months', '12 months'), ('6 months', '6 months'), ('3 months', '3 months'), ('1 month or less', '1 month or less')], default='12 months')
    category = RadioField(label='Category', choices=[('Full time', 'Full time'), ('Part time', 'Part time')], default='Full time')
    submit = SubmitField(label='Apply')

class Companysignupform(FlaskForm):
    name = StringField(label='Company Name', validators=[Length(min=2, max=100)])
    email = StringField(label='Company Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirmpassword = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign Up')

class Companyloginform(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=30)])
    submit = SubmitField(label='Login')