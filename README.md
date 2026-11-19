# Лабораторні роботи 3–7: Flask

Навчальний застосунок Flask з Blueprints, формами Flask-WTF, каталогом TinyDB, SQLAlchemy та Alembic міграціями.

## Запуск

```powershell
.\.venv\Scripts\Activate.ps1
Copy-Item .env.example .env  # один раз; задайте власний SECRET_KEY
python run.py
```

Вебзастосунок відкривається на `http://127.0.0.1:5000/`. Flask CLI використовує порт 8080 із `.flaskenv`.

## Лабораторна 5

- Контактна форма Flask-WTF: `/contact` і `/contacts`; валідні звернення додаються до `logs/contacts.log`.
- TinyDB каталог у `data/products.json`: список `/product`, створення `/product/add`, картка `/product/<id>`, редагування `/product/<id>/edit`, підтвердження видалення `/product/<id>/delete`.
- Перевіряються поля товару та завантаження зображення (PNG/JPG/JPEG, до 2 МБ). Зображення зберігаються в `app/products/static/uploads/`.
- Тести: `tests/test_contact_forms.py` і `tests/test_products.py`.

## Лабораторна 6

- Фабрика застосунку `create_app()` та конфігурації development/testing/production: `app/config.py`.
- SQLAlchemy та Flask-Migrate ініціалізуються в `app/extensions.py` та `app/__init__.py`.
- CRUD публікацій у Blueprint `app/posts/`: `/post`, `/post/create`, `/post/<id>`, `/post/<id>/update`, `/post/<id>/delete`.
- Модель `Post` і її міграції: `app/posts/models.py`, `migrations/versions/`.
- SQLite база зберігається в `instance/data.sqlite`.
- Тести: `tests/test_posts.py`.

## Лабораторна 7: зв'язки та міграції

Виконуйте кроки по порядку на гілці `lab7`. Ініціалізація Alembic уже виконана в репозиторії; повторно `flask db init` запускати не потрібно.

1. `Product` із полями `id`, `name`, `price` і первинна міграція: `7084b0b40de9_add_product.py`. Після `flask db upgrade` створіть у Flask shell записи `Pc` та `MAC`:

```python
from app.extensions import db
from app.products.models import Product

db.session.add_all([Product(name="Pc", price=700), Product(name="MAC", price=500)])
db.session.commit()
```

2. Додано `Category`, зв'язок один-до-багатьох і зовнішній ключ `products.category_id`. Після `flask db migrate -m "Add Category and Product relationship"` SQLite вимагає іменований ключ; міграція задає `fk_products_category_id_categories`, щоб працювали upgrade та downgrade: `91e83e832aa1_add_category_and_product_relationship.py`. Перевірте `flask db upgrade`, `flask db downgrade` і повторний `flask db upgrade`.
3. Naming convention для індексів і обмежень налаштовано на SQLAlchemy metadata в `app/extensions.py`. Виконайте `flask db check` та `flask db migrate -m "Add database constraint naming convention"`; нових змін схеми бути не повинно.
4. У `Product` додано `active` (NOT NULL, за замовчуванням True). Для вже наявних рядків міграція додає серверне значення `1`: `277ca243e721_add_active_flag_to_products.py`. Після змін моделі виконайте `flask db check`, `flask db migrate -m "Add active flag to products"` та `flask db upgrade`.
5. У Flask shell додайте `iPhone 15`, категорію `Laptops` та неактивний товар `Gaming Laptop`, прив'язаний до цієї категорії:

```python
from app.extensions import db
from app.products.models import Category, Product

laptops = Category(name="Laptops")
gaming = Product(name="Gaming Laptop", price=1500, active=False, category=laptops)
iphone = Product(name="iPhone 15", price=999.99)
db.session.add_all([laptops, gaming, iphone])
db.session.commit()
```

6. `created_at` має тип DateTime з часовою зоною, NOT NULL та `server_default=func.now()`. Міграція без серверного значення не проходить на непорожній SQLite таблиці; перевірте її наявних товарах, додайте тимчасовий `CURRENT_TIMESTAMP`, застосуйте і відкотіть цю ревізію, після чого згенеруйте фінальну міграцію з `func.now()`: `fc7f390f4c06_add_product_creation_timestamp_with_.py`.
7. Створіть ревізію командою `flask db revision -m "Insert sample product data"`. Ручна data migration додає приклад товару та категорії у `upgrade()` і прибирає їх у `downgrade()`: `fe91f634269e_insert_sample_product_data.py`.

Команди для перевірки міграцій:

```powershell
python -m flask db current
python -m flask db history
python -m flask db check
python -m flask db upgrade
```

Щоб повторити ручну data migration окремо, після перегляду поточного head виконайте `flask db downgrade fc7f390f4c06`, потім `flask db upgrade`; приклад з'явиться в `products` і `categories`.

## Тести

```powershell
python -m unittest discover tests -v
```

Перегляд історії комітів: `git log --oneline --decorate`.
