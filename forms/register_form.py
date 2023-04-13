from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, RadioField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    # TODO: Заменить на EmailField
    email = StringField("Электронная почта", validators=[DataRequired()])
    first_name = StringField("Имя", validators=[DataRequired(), Length(min=2)])
    second_name = StringField("Фамилия", validators=[DataRequired(), Length(min=2)])
    invite_code = StringField("Пригласительный код")
    remember = BooleanField("Запомнить меня")
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Зарегистрироваться")

