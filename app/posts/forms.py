from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeLocalField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

from app.posts.models import POST_CATEGORIES


class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(max=150)])
    content = TextAreaField("Текст поста", validators=[DataRequired()])
    enabled = BooleanField("Публікувати пост")
    publish_date = DateTimeLocalField("Дата й час публікації", format="%Y-%m-%dT%H:%M", default=datetime.now)
    category = SelectField("Категорія", choices=[(value, value.title()) for value in POST_CATEGORIES], validators=[DataRequired()])
    submit = SubmitField("Зберегти пост")


class DeletePostForm(FlaskForm):
    pass