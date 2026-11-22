from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from flask import abort, current_app, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from app.products import products_bp
from app.products.forms import DeleteProductForm, ProductForm
from app.products.store import add_product, all_products, delete_product, get_product, update_product


legacy_products = [
    {"id": 1, "name": "Laptop", "price": 1200, "content": "Потужний ноутбук з процесором Intel Core i7, 16 ГБ оперативної пам’яті та SSD на 512 ГБ."},
    {"id": 2, "name": "Phone", "price": 800, "content": "Смартфон із 6.5-дюймовим OLED-дисплеєм, подвійною камерою та акумулятором на 5000 мА·год."},
    {"id": 3, "name": "PC", "price": 1800, "content": "Настільний комп’ютер для ігор або роботи з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD."},
]


def _save_image(upload):
    if not upload or not upload.filename:
        return ""
    original_name = secure_filename(upload.filename)
    suffix = Path(original_name).suffix.lower()
    filename = f"{uuid4().hex}{suffix}"
    folder = Path(current_app.config["PRODUCT_UPLOAD_FOLDER"])
    folder.mkdir(parents=True, exist_ok=True)
    upload.save(folder / filename)
    return f"uploads/{filename}"


def _remove_image(relative_path):
    if not relative_path or not relative_path.startswith("uploads/"):
        return
    folder = Path(current_app.config["PRODUCT_UPLOAD_FOLDER"]).resolve()
    target = (folder / Path(relative_path).name).resolve()
    if target.parent == folder and target.exists():
        target.unlink()


def _required_product(product_id):
    product = get_product(product_id)
    if product is None:
        abort(404)
    return product


@products_bp.get("/products/")
def product_list():
    return render_template("products/products.html", title="Товари", products=legacy_products)


@products_bp.get("/products/<int:product_id>")
def detail_product(product_id):
    product = next((item for item in legacy_products if item["id"] == product_id), None)
    if product is None:
        abort(404)
    return render_template("products/detail_product.html", title=product["name"], product=product)


@products_bp.get("/product")
def all_products_page():
    return render_template("products/all_products.html", title="Каталог товарів", products=all_products())


@products_bp.route("/product/add", methods=["GET", "POST"])
def add_product_page():
    form = ProductForm()
    if form.validate_on_submit():
        image = _save_image(form.image.data)
        data = {
            "name": form.name.data.strip(),
            "content": form.content.data.strip(),
            "price": float(form.price.data.quantize(Decimal("0.01"))),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        add_product(data)
        flash("Товар успішно додано.", "success")
        return redirect(url_for("products.all_products_page"))
    return render_template("products/product_form.html", title="Додати товар", form=form, heading="Додати товар")


@products_bp.get("/product/<int:product_id>")
def product_detail_page(product_id):
    product = _required_product(product_id)
    return render_template("products/product_detail.html", title=product["name"], product=product)


@products_bp.route("/product/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product_page(product_id):
    product = _required_product(product_id)
    form = ProductForm(obj=type("ProductData", (), product)())
    if form.validate_on_submit():
        image = _save_image(form.image.data) or product.get("image", "")
        if image != product.get("image", ""):
            _remove_image(product.get("image", ""))
        changes = {
            "name": form.name.data.strip(),
            "content": form.content.data.strip(),
            "price": float(form.price.data.quantize(Decimal("0.01"))),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image,
        }
        update_product(product_id, changes)
        flash("Товар успішно оновлено.", "success")
        return redirect(url_for("products.product_detail_page", product_id=product_id))
    return render_template("products/product_form.html", title="Редагувати товар", form=form, heading="Редагувати товар")


@products_bp.route("/product/<int:product_id>/delete", methods=["GET", "POST"])
def delete_product_page(product_id):
    product = _required_product(product_id)
    form = DeleteProductForm()
    if form.validate_on_submit():
        delete_product(product_id)
        _remove_image(product.get("image", ""))
        flash("Товар видалено.", "success")
        return redirect(url_for("products.all_products_page"))
    return render_template("products/delete_confirm.html", title="Підтвердження видалення", product=product, form=form)
