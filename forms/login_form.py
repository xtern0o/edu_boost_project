from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    # TODO: Заменить на EmailField
    email = StringField("Электронная почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")