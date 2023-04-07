from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length
from flask import url_for


class ChatForm(FlaskForm):
    message = StringField("Сообщение")
    submit = SubmitField()
