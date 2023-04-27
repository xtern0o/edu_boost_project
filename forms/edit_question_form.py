from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length


class EditQuestionForm(FlaskForm):
    question_id = StringField()
    title = StringField('Заголовок', validators=[DataRequired()])
    text = StringField('Вопрос', validators=[DataRequired()])
    correct_answer = StringField('Правильный ответ', validators=[DataRequired()])
    points = IntegerField('Баллы', validators=[DataRequired()])
    submit = SubmitField('Изменить')
    delete = SubmitField('Удалить')