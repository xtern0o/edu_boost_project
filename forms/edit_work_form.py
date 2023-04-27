from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DateTimeField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField, TimeField


class EditWorkForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    deadline = DateTimeLocalField("Дата сдачи", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    submit = SubmitField("Изменить")
