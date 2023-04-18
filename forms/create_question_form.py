from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, Length


class CreateQuestionForm(FlaskForm):
    name = StringField("Название группы", validators=[DataRequired()])
    text = StringField("Текст вопроса")
    correct_answer = StringField("Правильный ответ")
    submit = SubmitField("Создать")