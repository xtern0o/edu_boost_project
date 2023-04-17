from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, StringField
from wtforms.validators import DataRequired


class InviteForm(FlaskForm):
    email = EmailField()
    submit = SubmitField('Отправить приглашение')


class JoinGroupForm(FlaskForm):
    code = StringField()
    submit = SubmitField('Вступить в группу')
