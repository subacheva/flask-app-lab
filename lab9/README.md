# Лабораторна 9 — Побудова системи реєстрації та входу

Окремий Flask-застосунок з Flask-Bcrypt і Flask-Login. Модель користувача пов’язана з постами з лабораторної 8.

## Запуск

Перейди в каталог lab9, встанови залежності, застосуй міграції та запусти Flask:

    cd lab9
    pip install -r requirements.txt
    flask db upgrade
    flask run

## Реєстрація та вхід

- /register перевіряє username та email, у тому числі унікальність, хешує пароль через Flask-Bcrypt, зберігає користувача і виконує автоматичний вхід;
- /login перевіряє введений пароль через Bcrypt;
- /account показує дані current_user і доступний після входу;
- /users показує всіх користувачів і їхню кількість; доступ захищений login_required;
- /logout виконує logout_user та завершує сесію;
- меню змінюється відповідно до current_user.is_authenticated.

## Тести

    python -m unittest discover tests -v