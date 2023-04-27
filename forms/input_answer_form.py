from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, Length


class InputAnswerForm(FlaskForm):
    answer = StringField("Ответ", validators=[DataRequired()])
    submit = SubmitField("Сохранить")

