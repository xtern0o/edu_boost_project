from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DateTimeField
from wtforms.validators import DataRequired, Length


class EditWorkForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    deadline = DateTimeField(validators=[DataRequired()])
    submit = SubmitField("Изменить название")
