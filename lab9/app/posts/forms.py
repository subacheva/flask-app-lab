from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeLocalField, SelectField, SelectMultipleField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

from app.extensions import db
from app.models import Tag, User


class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(max=150)])
    content = TextAreaField("Текст", validators=[DataRequired()])
    publish_date = DateTimeLocalField("Дата та час", format="%Y-%m-%dT%H:%M", default=datetime.now)
    category = SelectField("Категорія", choices=[("news", "Новина"), ("publication", "Публікація"), ("tech", "Технології"), ("other", "Інше")], validators=[DataRequired()])
    author_id = SelectField("Автор", coerce=int, validators=[DataRequired()])
    tags = SelectMultipleField("Теги", coerce=int)
    enabled = BooleanField("Опубліковано", default=True)
    submit = SubmitField("Зберегти")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_id.choices = [(user.id, user.username) for user in db.session.query(User).order_by(User.id)]
        self.tags.choices = [(tag.id, tag.name) for tag in db.session.query(Tag).order_by(Tag.name)]


class UserForm(FlaskForm):
    username = StringField("Ім’я користувача", validators=[DataRequired(), Length(max=80)])
    email = StringField("Email", validators=[DataRequired(), Length(max=254)])
    password = StringField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Додати користувача")


class TagForm(FlaskForm):
    name = StringField("Назва тегу", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Додати тег")
