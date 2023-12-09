from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    submit = SubmitField('Logar')