from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField


class CreateWorkForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    info = TextAreaField("Описание группы", validators=[DataRequired()])
    deadline = DateTimeLocalField("qwe", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    submit = SubmitField("Создать новый тест")
