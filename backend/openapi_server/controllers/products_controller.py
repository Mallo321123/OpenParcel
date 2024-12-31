import connexion
from openapi_server.models.products import Products  # noqa: E501
from openapi_server.models.products_response import ProductsResponse  # noqa: E501

from openapi_server.db import get_db, close_db
from openapi_server.tokenManager import valid_token
from openapi_server.permission_check import check_permission

from flask_jwt_extended import jwt_required, get_jwt
from flask import request

from typing import Optional

from openapi_server.security import check_sql_inject_value, check_sql_inject_json

import json
from rapidfuzz import process, fuzz


@jwt_required()
def product_add(products=None):  # noqa: E501
    jwt_data = get_jwt()
    user = jwt_data.get("user")

    if not (check_permission("products", user) or check_permission("admin", user)):
        return "unauthorized", 401

    token = request.headers.get("Authorization").split(" ")[1]

    if not valid_token(user, token):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    if connexion.request.is_json:
        products = Products.from_dict(connexion.request.get_json())  # noqa: E501
        
        if check_sql_inject_json(products):
            return "Invalid input", 400

        cursor.execute("SELECT * FROM products WHERE name = %s", (products.name,))
        if cursor.fetchone() is not None:
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
            return str(e), 400

        db.commit()
        close_db(db)

        return "Product created", 200


@jwt_required()
def products_delete(id):  # noqa: E501
    jwt_data = get_jwt()
    user = jwt_data.get("user")

    if not (check_permission("products", user) or check_permission("admin", user)):
        return "unauthorized", 401

    token = request.headers.get("Authorization").split(" ")[1]

    if not valid_token(user, token):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()
    
    if check_sql_inject_value(id):
        return "Invalid input", 400

    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    if cursor.fetchone() is None:
        return "Product not found", 400

    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    db.commit()

    close_db(db)
    return "Product deleted", 200


@jwt_required()
def products_list(limit=None, page=None):  # noqa: E501
    jwt_data = get_jwt()
    user = jwt_data.get("user")

    token = request.headers.get("Authorization").split(" ")[1]

    if not valid_token(user, token):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()
    
    if check_sql_inject_value(limit) or check_sql_inject_value(page):
        return "Invalid input", 400

    offset = limit * page

    cursor.execute(
        "SELECT * FROM products ORDER BY id ASC LIMIT %s OFFSET %s", (limit, offset)
    )
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
def update_product(name, products=None):  # noqa: E501
    jwt_data = get_jwt()
    user = jwt_data.get("user")

    if not (check_permission("products", user) or check_permission("admin", user)):
        return "unauthorized", 401

    token = request.headers.get("Authorization").split(" ")[1]

    if not valid_token(user, token):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()
    
    if check_sql_inject_value(name):
        return "Invalid input", 400

    if connexion.request.is_json:
        products = Products.from_dict(connexion.request.get_json())  # noqa: E501
        
        if check_sql_inject_json(products):
            return "Invalid input", 400

        if isinstance(products, Products):
            products = products.to_dict()

        # Prepare a dictionary of fields to update
        update_fields = {}

        if products.get("buildTime") is not None:
            update_fields["buildTime"] = products["BuildTime"]

        if products.get("comment") is not None:
            update_fields["comment"] = products["comment"]

        if products.get("customerGroups") is not None:
            customer_groups_json = json.dumps(products["customerGroups"])
            update_fields["customerGroups"] = customer_groups_json

        if products.get("difficulty") is not None:
            update_fields["difficulty"] = products["difficulty"]

        if products.get("name") is not None:
            cursor.execute(
                "SELECT * FROM products WHERE name = %s", (products["name"],)
            )
            if cursor.fetchone() is not None:
                return "Name already taken", 400
            update_fields["name"] = products["name"]

        if update_fields is None:
            return "No fields to update", 400

        # Construct the SQL update statement dynamically
        set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
        values = list(update_fields.values())
        values.append(name)

        update_query = f"UPDATE products SET {set_clause} WHERE name = %s"

        try:
            cursor.execute(update_query, tuple(values))
            db.commit()
        except Exception as e:
            db.rollback()
            return f"Failed to update product: {e}", 500
        finally:
            close_db(db)

        return "Product updated", 200
    return "Invalid input", 400


@jwt_required()
def products_info_get():  # noqa: E501
    jwt_data = get_jwt()
    user = jwt_data.get("user")

    id = request.args.get("id")

    token = request.headers.get("Authorization").split(" ")[1]

    if not valid_token(user, token):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()
    
    if check_sql_inject_value(id):
        return "Invalid input", 400

    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cursor.fetchone()

    close_db(db)

    if product is None:
        return "Product not found", 400

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
    jwt_data = get_jwt()
    user = jwt_data.get("user")  # Extract username from token
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return "unauthorized", 401
    token = auth_header.split(" ")[1]  # Extract token

    if not valid_token(user, token):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()
    
    if check_sql_inject_value(limit) or check_sql_inject_value(page):
        return "Invalid input", 400
    
    if check_sql_inject_value(name) or check_sql_inject_value(difficulty) or check_sql_inject_value(sort) or check_sql_inject_value(order):
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

        if sort not in ALLOWED_SORT_COLUMNS or order.lower() not in ALLOWED_ORDER_DIRECTIONS:
            return "Invalid sort or order parameter", 400

        query = f"SELECT * FROM products ORDER BY {sort} {order.upper()} LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, offset))
        products = cursor.fetchall()

    elif difficulty is not None and sort is not None and order is not None:
        ALLOWED_SORT_COLUMNS = {"name", "difficulty", "build_time"}
        ALLOWED_ORDER_DIRECTIONS = {"asc", "desc"}

        if sort not in ALLOWED_SORT_COLUMNS or order.lower() not in ALLOWED_ORDER_DIRECTIONS:
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
