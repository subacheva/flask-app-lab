# Flask labs 3–7

Навчальний Flask-застосунок із Blueprints, формами, TinyDB, SQLAlchemy та міграціями.

## Запуск

```powershell
.\.venv\Scripts\Activate.ps1
Copy-Item .env.example .env  # один раз; задайте власний SECRET_KEY
python run.py
```

Сайт працює на `http://127.0.0.1:5000/` (Flask CLI використовує порт 8080 із `.flaskenv`). Для Flask CLI потрібні залежності з `requirements.txt`.

## Лабораторна 5

- Контактна форма з Flask-WTF: `/contact` або `/contacts`; валідні звернення додаються до `logs/contacts.log`.
- TinyDB JSON-каталог: `/product`; створення `/product/add`; деталі `/product/<id>`; редагування `/product/<id>/edit`; підтвердження/видалення `/product/<id>/delete`.
- Дані: `data/products.json`; завантажені картинки: `app/products/static/uploads/` (до 2 МБ, PNG/JPG/JPEG).

## Лабораторна 6

- Application factory: `create_app("development")`, `create_app("testing")` або `create_app("production")`.
- SQLite-файл створюється в `instance/data.sqlite`.
- Пост-маршрути: `/post`, `/post/create`, `/post/<id>`, `/post/<id>/update`, `/post/<id>/delete`.
- Перше налаштування міграцій (виконати один раз):

```powershell
flask --app run.py db init
flask --app run.py db migrate -m "Initial posts table"
flask --app run.py db upgrade
flask --app run.py db migrate -m "Add post status and author"
flask --app run.py db upgrade
```

Після зміни моделей створюйте нову міграцію через `flask --app run.py db migrate -m "опис зміни"`, перевіряйте її, а потім застосовуйте `flask --app run.py db upgrade`.

## Лабораторна 7

Використовуйте поточну гілку `lab7`. Вона додає SQLAlchemy Product/Category із зовнішнім ключем, naming convention, еволюцію схеми та ручну data migration.

## Тести

```powershell
python -m unittest discover tests -v
```

Відкрити історію Git-комітів: `git log --oneline --decorate`.