from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length


class CreateQuestionForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    text = StringField(validators=[DataRequired()])
    correct_answer = StringField(validators=[DataRequired()])
    points = IntegerField(validators=[DataRequired()])
    submit = SubmitField("Создать вопрос")