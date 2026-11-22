from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField("Ім’я", validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField("Електронна пошта", validators=[DataRequired(), Email(), Length(max=120)])
    topic = SelectField(
        "Тема звернення",
        choices=[("internship", "Стажування"), ("project", "Проєкт"), ("other", "Інше")],
        validators=[DataRequired()],
    )
    message = TextAreaField("Повідомлення", validators=[DataRequired(), Length(min=10, max=4000)])
    submit = SubmitField("Надіслати повідомлення")
