from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, EmailField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = EmailField("Электронная почта", validators=[DataRequired(), Email("Некорректная почта")])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")