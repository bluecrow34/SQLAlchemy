from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional


class UserAddForm (FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1,max=20)])
    password = StringField("Password", validators=[InputRequired(), Length(min=4,max=50)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1,max=20)])
    password = StringField("Password", validators=[InputRequired(), Length(min=4,max=50)])
    

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])
    username = StringField()

class DeleteFrom(FlaskForm):
    """Delete Form"""