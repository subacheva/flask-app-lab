from pathlib import Path

from tinydb import TinyDB


def _database():
    from flask import current_app

    path = Path(current_app.config["TINYDB_PATH"])
    path.parent.mkdir(parents=True, exist_ok=True)
    return TinyDB(path)


def all_products():
    database = _database()
    try:
        records = database.table("products").all()
    finally:
        database.close()
    return sorted(records, key=lambda product: product.get("created_at", ""), reverse=True)


def get_product(product_id):
    database = _database()
    try:
        return database.table("products").get(doc_id=product_id)
    finally:
        database.close()


def add_product(product):
    database = _database()
    try:
        table = database.table("products")
        product_id = table.insert(product)
        table.update({"id": product_id}, doc_ids=[product_id])
        return product_id
    finally:
        database.close()


def update_product(product_id, changes):
    database = _database()
    try:
        return database.table("products").update(changes, doc_ids=[product_id])
    finally:
        database.close()


def delete_product(product_id):
    database = _database()
    try:
        return database.table("products").remove(doc_ids=[product_id])
    finally:
        database.close()
