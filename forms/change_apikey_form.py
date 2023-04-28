from flask_wtf import FlaskForm
from wtforms import SubmitField


class ChangeApikey(FlaskForm):
    change = SubmitField("Сменить API-ключ")
