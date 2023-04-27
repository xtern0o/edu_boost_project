from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, EmailField
from wtforms.validators import DataRequired, Length, Email


class PublishWorkForm(FlaskForm):
    work_id = StringField()
    submit = SubmitField("Опубликовать")