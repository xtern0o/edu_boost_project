from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField, TimeField


class CreateWorkForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    info = TextAreaField("Описание группы", validators=[DataRequired()])
    deadline = DateTimeLocalField("Дата сдачи", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    time = TimeField('Время выполнения', validators=[DataRequired()])
    group = SelectField('Группа', validators=[DataRequired()])
    submit = SubmitField("Создать новый тест")
