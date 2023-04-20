from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, Length


class EditNameWorkForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField("Изменить название")
