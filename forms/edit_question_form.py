from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired, Length


class EditTitleQuestionForm(FlaskForm):
    question_id = StringField()
    title = StringField(validators=[DataRequired()])
    submit = SubmitField('Изменить')


class EditTextQuestionForm(FlaskForm):
    question_id = StringField()
    text = StringField(validators=[DataRequired()])
    submit = SubmitField('Изменить')


class EditCorrectAnswerQuestionForm(FlaskForm):
    question_id = StringField()
    correct_answer = StringField(validators=[DataRequired()])
    submit = SubmitField('Изменить')