from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, DateTimeField, SelectField
from wtforms.fields.html5 import DateTimeField, DateTimeLocalField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILES = ["PNG", "JPG", "png", "jpg", "JPEG", "jpeg"]

# creates the login information


class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])


# registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           InputRequired(), Email("Please enter a valid email")])
    contact = IntegerField("Contact Number", validators=[
                           InputRequired('Please enter a valid contact number')])
    address = StringField("Address", validators=[
                          InputRequired('Please enter your address')])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo(
        'confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])

# create event form
class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[InputRequired()])
    artist_name = StringField('Artist Name', validators=[InputRequired()])
    status = SelectField("Status", choices=[("", "--Please select status--"),
                                            ("Active", "Active"), ("Upcoming", "Upcoming"), ("Inactive", "Inactive")])
    genre = SelectField("Genre", choices=[("", "--Please select genre--"), ("Country", "Country"), ("Electronic", "Electronic"),
                                          ("Funk", "Funk"), ("Hiphop", "Hip Hop"), ("Jazz", "Jazz"), ("House", "House"), 
                                          ("Pop", "Pop"), ("Rap", "Rap"), ("Rock", "Rock")])
    datetime = StringField('Date and Time', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    google_map = StringField('Google Map Link', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Event Image', validators=[FileRequired(), FileAllowed(
        ALLOWED_FILES, message=f"Accepted file types: {ALLOWED_FILES}")])
    price = StringField('Price', validators=[InputRequired()])
    num_tickers = IntegerField(
        "Number of Tickets", validators=[InputRequired()])
    submit = SubmitField()

# edit event form
class EventEditForm(FlaskForm):
    event_name = StringField('Event Name', validators=[])
    artist_name = StringField('Artist Name', validators=[])
    status = SelectField("Status", choices=[("", "--Please select status--"),
                                            ("Active", "Active"), ("Upcoming", "Upcoming"), ("Inactive", "Inactive")])
    genre = SelectField("Genre", choices=[("", "--Please select genre--"), ("Country", "Country"), ("Electronic", "Electronic"),
                                          ("Funk", "Funk"), ("Hiphop", "Hip Hop"), ("Jazz", "Jazz"), ("House", "House"), 
                                          ("Pop", "Pop"), ("Rap", "Rap"), ("Rock", "Rock")])
    datetime = StringField('Date and Time', validators=[])
    location = StringField('Location', validators=[])
    description = TextAreaField('Description', validators=[])
    image = FileField('Event Image', validators=[FileAllowed(
        ALLOWED_FILES, message=f"Accepted file types: {ALLOWED_FILES}")])
    price = IntegerField('Price', validators=[Optional()])
    num_tickers = IntegerField(
        "Number of Tickets", validators=[Optional()])
    submit = SubmitField()

# comment form
class CommentForm(FlaskForm):
    text = StringField('Leave a comment here!', validators=[InputRequired()])
    submit = SubmitField('Create')


class BookingForm(FlaskForm):
    num_tickets = IntegerField(
        'Number of Tickets', validators=[InputRequired()])
    submit = SubmitField()
