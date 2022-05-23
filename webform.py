from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

# Create A Search Form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create PostForm
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    # content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    content = CKEditorField('Content', validators=[DataRequired()])
    # author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    button = SubmitField("Submit")


class PasswordForm(FlaskForm):
    email = StringField("What's your name", validators=[DataRequired()])
    password_hash = PasswordField("What's your password", validators=[DataRequired()])
    button = SubmitField("Submit")


# Create LoginForm
class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired(), Length(min=6, max=20) ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    favorite_color = StringField("Favorite Color")
    about_author = TextAreaField("About Author")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Mutch')])
    password_hash2 =PasswordField('Confirm Password', validators=[DataRequired()])
    profile_pic = FileField("Profile Pic")
    button = SubmitField("Submit")
