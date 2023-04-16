from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField
from wtforms.validators import DataRequired


class InviteForm(FlaskForm):
    email = EmailField()
    submit = SubmitField('Отправить приглашение')