import connexion
from openapi_server.models.products import Products  # noqa: E501
from openapi_server.models.products_response import ProductsResponse  # noqa: E501

from openapi_server.db import get_db, close_db
from flask_jwt_extended import jwt_required
from typing import Optional

from flask import request

from openapi_server.security import (
    check_sql_inject_value,
    check_sql_inject_json,
    check_auth,
)
import json
from rapidfuzz import process, fuzz
from openapi_server.config import get_logging

logging = get_logging()


@jwt_required()
def product_add(products=None):  # noqa: E501
    if not check_auth("products"):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    if connexion.request.is_json:
        products = Products.from_dict(connexion.request.get_json())  # noqa: E501

        if check_sql_inject_json(**products.to_dict()):
            return "Invalid input", 400

        cursor.execute("SELECT * FROM products WHERE name = %s", (products.name,))
        if cursor.fetchone() is not None:
            logging.warning(f"Product {products.name} already exists")
            return "Product already exists", 400

        customer_groups_json = json.dumps(products.customer_groups)

        try:
            cursor.execute(
                """INSERT INTO products 
                       (name, comment, customerGroups, difficulty, buildTime) VALUES (%s, %s, %s, %s, %s)""",
                (
                    products.name,
                    products.comment,
                    customer_groups_json,
                    products.difficulty,
                    products.build_time,
                ),
            )

        except Exception as e:
            logging.error(f"Failed to create product: {e}")
            return "Failed, check Server Log", 500

        db.commit()
        close_db(db)
        logging.info(f"Product {products.name} created")
        return "Product created", 200


@jwt_required()
def products_delete():  # noqa: E501
    if not check_auth("products"):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()
    
    id = request.args.get("id")

    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    if cursor.fetchone() is None:
        logging.warning(f"Product {id} not found")
        return "Product not found", 404

    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    db.commit()

    close_db(db)
    logging.info(f"Product {id} deleted")
    return "Product deleted", 200


@jwt_required()
def products_list(limit=None, page=None):  # noqa: E501
    if not check_auth():
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    offset = limit * page

    cursor.execute(
        "SELECT * FROM products ORDER BY id ASC LIMIT %s OFFSET %s", (limit, offset)
    )
    if cursor.fetchone() is None:
        logging.warning("No products found in products_list")
        return "No products found", 404
    
    products = cursor.fetchall()

    close_db(db)

    for i in range(len(products)):
        try:
            customerGroups = json.loads(products[i][3])
        except TypeError:
            customerGroups = []

        products[i] = ProductsResponse(
            id=products[i][0],
            name=products[i][1],
            comment=products[i][2],
            customer_groups=customerGroups,
            difficulty=products[i][4],
            build_time=products[i][5],
        )

    return products, 200


@jwt_required()
def update_product(products=None):  # noqa: E501
    if not check_auth("products"):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    id = request.args.get("id")

    if connexion.request.is_json:
        products = Products.from_dict(connexion.request.get_json())  # noqa: E501

        if check_sql_inject_json(**products.to_dict()):
            return "Invalid input", 400

        if isinstance(products, Products):
            products = products.to_dict()

        # Prepare a dictionary of fields to update
        update_fields = {}

        if products.get("build_time") is not None:
            update_fields["buildTime"] = products["build_time"]

        if products.get("comment") is not None:
            update_fields["comment"] = products["comment"]

        if products.get("customer_groups") is not None:
            customer_groups_json = json.dumps(products["customer_groups"])
            update_fields["customerGroups"] = customer_groups_json

        if products.get("difficulty") is not None:
            update_fields["difficulty"] = int(products["difficulty"])

        if products.get("name") is not None:
            cursor.execute(
                "SELECT * FROM products WHERE name = %s", (products["name"],)
            )
            if cursor.fetchone() is not None:
                return "Name already taken", 400
            update_fields["name"] = products["name"]

        if update_fields is None:
            logging.info("No fields to update in product_update")
            return "No fields to update", 400

        # Construct the SQL update statement dynamically
        set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
        values = list(update_fields.values())
        values.append(int(id))

        update_query = f"UPDATE products SET {set_clause} WHERE id = %s"

        try:
            cursor.execute(update_query, tuple(values))
            db.commit()
        except Exception as e:
            db.rollback()
            logging.error(f"Failed to update product: {e}")
            return "Failed to update product", 500
        finally:
            close_db(db)

        logging.info(f"Product with id {id} updated")
        return "Product updated", 200

    logging.warning("Invalid input in product_update")
    return "Invalid input", 400


@jwt_required()
def products_info_get():  # noqa: E501
    if not check_auth():
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    id = request.args.get("id")

    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    
    product = cursor.fetchone()

    close_db(db)

    if product is None:
        logging.warning(f"Product {id} not found")
        return "Product not found", 404

    try:
        customerGroups = json.loads(product[3])
    except TypeError:
        customerGroups = []

    product = ProductsResponse(
        id=product[0],
        name=product[1],
        comment=product[2],
        customer_groups=customerGroups,
        difficulty=product[4],
        build_time=product[5],
    )

    return product, 200


def sort_by_similarity(entries, input_name):
    names = [entry[1] for entry in entries]  # Extrahiert nur die Namen
    results = process.extract(input_name, names, scorer=fuzz.ratio)

    # Sortiere die Einträge nach der Übereinstimmung und behalte nur die relevanten Daten
    sorted_entries = [entries[names.index(result[0])] for result in results]

    return sorted_entries


@jwt_required()
def products_list_get(
    limit,
    page,
    name: Optional[str] = None,
    difficulty: Optional[int] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
):  # noqa: E501
    if not check_auth():
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    if (
        check_sql_inject_value(name)
        or check_sql_inject_value(difficulty)
        or check_sql_inject_value(sort)
        or check_sql_inject_value(order)
    ):
        return "Invalid input", 400

    offset = limit * page

    if name is not None:
        cursor.execute("SELECT * FROM products")
        
        products = cursor.fetchall()

        sorted_products = sort_by_similarity(products, name)
        products = sorted_products[offset : offset + limit]

    elif difficulty is not None:
        cursor.execute(
            "SELECT * FROM products WHERE difficulty = %s LIMIT %s OFFSET %s",
            (difficulty, limit, offset),
        )
        
        products = cursor.fetchall()

    elif sort is not None and order is not None:
        ALLOWED_SORT_COLUMNS = {"name", "difficulty", "build_time"}
        ALLOWED_ORDER_DIRECTIONS = {"asc", "desc"}

        if (
            sort not in ALLOWED_SORT_COLUMNS
            or order.lower() not in ALLOWED_ORDER_DIRECTIONS
        ):
            return "Invalid sort or order parameter", 400

        query = (
            f"SELECT * FROM products ORDER BY {sort} {order.upper()} LIMIT %s OFFSET %s"
        )
        cursor.execute(query, (limit, offset))
        products = cursor.fetchall()

    elif difficulty is not None and sort is not None and order is not None:
        ALLOWED_SORT_COLUMNS = {"name", "difficulty", "build_time"}
        ALLOWED_ORDER_DIRECTIONS = {"asc", "desc"}

        if (
            sort not in ALLOWED_SORT_COLUMNS
            or order.lower() not in ALLOWED_ORDER_DIRECTIONS
        ):
            return "Invalid sort or order parameter", 400

        query = (
            f"SELECT * FROM products WHERE difficulty = %s ORDER BY {sort} {order.upper()} "
            "LIMIT %s OFFSET %s"
        )
        cursor.execute(query, (difficulty, limit, offset))
        products = cursor.fetchall()
    else:
        return "Invalid input", 400

    close_db(db)
    
    if products is None:
        logging.warning("No products found in products_list_get")
        return "No products found", 404

    for i in range(len(products)):
        try:
            customerGroups = json.loads(products[i][3])
        except TypeError:
            customerGroups = []
        products[i] = ProductsResponse(
            id=products[i][0],
            name=products[i][1],
            comment=products[i][2],
            customer_groups=customerGroups,
            difficulty=products[i][4],
            build_time=products[i][5],
        )

    return products, 200
