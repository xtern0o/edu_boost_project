from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, RadioField, EmailField
from wtforms.validators import DataRequired, Length, Email


class StartWorkForm(FlaskForm):
    work_id = StringField()
    action = StringField()
    submit = SubmitField('Начать')