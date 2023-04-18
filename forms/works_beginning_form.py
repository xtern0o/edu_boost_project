from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, RadioField
from wtforms.validators import DataRequired, Length


class WorksBeginningForm(FlaskForm):
	start = SubmitField("Начать прохождение")