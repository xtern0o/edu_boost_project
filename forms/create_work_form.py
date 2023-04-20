from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, Length


class CreateWorkForm(FlaskForm):
    name = StringField("Название группы", validators=[DataRequired()])
    submit = SubmitField("Создать новый тест")