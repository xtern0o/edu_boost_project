from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, Length


class GroupCreatingForm(FlaskForm):
    name = StringField("Название группы", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Создать")

