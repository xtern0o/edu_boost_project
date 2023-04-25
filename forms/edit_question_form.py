from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length


class EditQuestionForm(FlaskForm):
    question_id = StringField()
    title = StringField(validators=[DataRequired()])
    text = StringField(validators=[DataRequired()])
    correct_answer = StringField(validators=[DataRequired()])
    points = IntegerField(validators=[DataRequired()])
    submit = SubmitField('Изменить')