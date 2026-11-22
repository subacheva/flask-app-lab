from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.extensions import db
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Ім’я користувача", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Електронна пошта", validators=[DataRequired(), Email(), Length(max=254)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Повторіть пароль", validators=[DataRequired(), EqualTo("password", message="Паролі мають збігатися.")])
    submit = SubmitField("Зареєструватися")

    def validate_username(self, field):
        if db.session.scalar(select(User.id).where(User.username == field.data.strip())):
            raise ValidationError("Це ім’я користувача вже зайняте.")

    def validate_email(self, field):
        if db.session.scalar(select(User.id).where(User.email == field.data.strip().lower())):
            raise ValidationError("Ця електронна адреса вже зареєстрована.")


class LoginForm(FlaskForm):
    email = StringField("Електронна пошта", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Увійти")
