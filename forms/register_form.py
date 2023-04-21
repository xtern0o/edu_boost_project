from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, RadioField, EmailField
from wtforms.validators import DataRequired, Length, Email


class RegisterForm(FlaskForm):
    # TODO: Заменить на EmailField
    email = EmailField("Электронная почта", validators=[DataRequired(), Email("Некорректная почта")])
    first_name = StringField("Имя", validators=[DataRequired(), Length(min=2)])
    second_name = StringField("Фамилия", validators=[DataRequired(), Length(min=2)])
    invite_code = StringField("Пригласительный код")
    remember = BooleanField("Запомнить меня")
    password = PasswordField("Пароль", validators=[DataRequired(), Length(message="Минимальная длина пароля - 6 символов", min=6)])
    submit = SubmitField("Зарегистрироваться")

