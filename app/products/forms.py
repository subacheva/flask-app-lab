from decimal import Decimal

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import DecimalField, FileField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange


PRODUCT_CATEGORIES = [
    ("electronics", "Електроніка"),
    ("books", "Книги"),
    ("home", "Для дому"),
    ("other", "Інше"),
]


class ProductForm(FlaskForm):
    name = StringField("Назва товару", validators=[DataRequired(), Length(min=3, max=120)])
    content = TextAreaField("Опис", validators=[DataRequired(), Length(min=5, max=4000)])
    price = DecimalField(
        "Ціна",
        places=2,
        rounding=None,
        validators=[DataRequired(), NumberRange(min=Decimal("0.01"))],
    )
    category = SelectField("Категорія", choices=PRODUCT_CATEGORIES, validators=[DataRequired()])
    quantity = IntegerField("Кількість", validators=[InputRequired(), NumberRange(min=0)])
    image = FileField("Зображення (PNG, JPG або JPEG)", validators=[FileAllowed(["png", "jpg", "jpeg"], "Дозволено PNG, JPG та JPEG.")])
    submit = SubmitField("Зберегти")

class DeleteProductForm(FlaskForm):
    pass
