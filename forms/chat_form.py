from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask import url_for


class ChatForm(FlaskForm):
    message = TextAreaField()
