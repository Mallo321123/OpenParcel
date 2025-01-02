import connexion

from openapi_server.models.orders_add import OrdersAdd  # noqa: E501
from openapi_server.models.orders_response import OrdersResponse
from openapi_server.models.orders_response_item import OrdersResponseItem
from openapi_server.models.orders_change import OrdersChange

from openapi_server.db import get_db, close_db

from flask import request, jsonify
from flask_jwt_extended import jwt_required

from typing import Optional

from openapi_server.security import (
    check_sql_inject_value,
    check_sql_inject_json,
    check_auth,
)

import json
import datetime

from openapi_server.config import get_logging

logging = get_logging()


@jwt_required()
def orders_delete():  # noqa: E501
    if not check_auth("orders"):
        return "unauthorized", 401

    id = request.args.get("id")

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders WHERE id = %s", (id,))
    result = cursor.fetchone()
    if result is None:
        logging.warning(f"Order {id} not found")
        return "Order not found", 404

    cursor.execute("DELETE FROM orders WHERE id = %s", (id,))
    db.commit()
    close_db(db)

    logging.info(f"Order {id} deleted")
    return "Order deleted", 200


@jwt_required()
def orders_get(limit=None, page=None):  # noqa: E501
    if not check_auth():
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    offset = limit * page if limit and page else 0

    cursor.execute("SELECT COUNT(*) AS total_orders FROM orders")
    total_items = cursor.fetchone()[0]

    cursor.execute(
        "SELECT * FROM orders ORDER BY id DESC LIMIT %s OFFSET %s", (limit, offset)
    )
    orders = cursor.fetchall()
    close_db(db)

    items = []
    for order in orders:
        date_closed = order[3] if order[3] is not None else "-"
        products = json.loads(order[4].replace("'", '"'))

        item = {
            "id": order[0],
            "customer": order[1],
            "dateAdd": order[2],
            "dateClosed": date_closed,
            "comment": order[5],
            "products": products,
            "state": order[6],
            "shipmentType": order[7],
        }
        items.append(item)

    # JSON-Response erstellen
    response = {"items": items, "totalItems": total_items}

    return jsonify(response), 200


@jwt_required()
def orders_post(orders_add=None):  # noqa: E501
    if not check_auth("orders"):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    if connexion.request.is_json:
        orders_add = OrdersAdd.from_dict(connexion.request.get_json())  # noqa: E501

        if check_sql_inject_json(**orders_add.to_dict()):
            return "Invalid input", 400

        cursor.execute(
            """INSERT INTO orders 
                   (customer, addDate, products, comment, state, shipmentType) VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                orders_add.customer,
                datetime.datetime.now(),
                str(orders_add.products),
                orders_add.comment,
                orders_add.state,
                orders_add.shipment_type,
            ),
        )

        db.commit()
        close_db(db)
        logging.info("Order added")
        return "Order added", 201

    logging.warning("Invalid request in orders_post")
    return "invalid request", 400


@jwt_required()
def orders_put(orders_change=None):  # noqa: E501
    if not check_auth("orders"):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    id = request.args.get("id")

    cursor.execute("SELECT * FROM orders WHERE id = %s", (id,))
    result = cursor.fetchone()
    if result is None:
        return "Order not found", 404

    if connexion.request.is_json:
        orders_change = OrdersChange.from_dict(connexion.request.get_json())  # noqa: E501

        if isinstance(orders_change, OrdersChange):
            orders_change = orders_change.to_dict()

        if check_sql_inject_json(**orders_change):
            return "Invalid input", 400

        update_fields = {}

        if orders_change.get("date_add") is not None:
            update_fields["addDate"] = orders_change["date_add"]

        if orders_change.get("state") is not None:
            update_fields["state"] = orders_change["state"]

        if orders_change.get("shipment_type") is not None:
            update_fields["shipmentType"] = orders_change["shipment_type"]

        if orders_change.get("comment") is not None:
            update_fields["comment"] = orders_change["comment"]

        if orders_change.get("products") is not None:
            update_fields["products"] = str(orders_change["products"])

        if orders_change.get("customer") is not None:
            update_fields["customer"] = orders_change["customer"]

        if orders_change.get("date_closed") is not None:
            update_fields["closeDate"] = orders_change["date_closed"]

        if update_fields is None:
            return "No fields to update", 400

        # Construct the SQL update statement dynamically
        set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
        values = list(update_fields.values())
        values.append(id)

        update_query = f"UPDATE orders SET {set_clause} WHERE id = %s"

        cursor.execute(update_query, tuple(values))
        db.commit()
        close_db(db)
        logging.info(f"Order {id} updated")
        return "ok", 200

    logging.warning("Invalid request in orders_put")
    return "invalid request", 400


@jwt_required()
def orders_list_get(
    limit,
    page,
    state: Optional[str] = None,
    customer: Optional[str] = None,
    shipment: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
):  # noqa: E501
    if not check_auth():
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    offset = limit * page if limit and page else 0

    if (
        check_sql_inject_value(state)
        or check_sql_inject_value(customer)
        or check_sql_inject_value(shipment)
        or check_sql_inject_value(sort)
        or check_sql_inject_value(order)
    ):
        return "Invalid input", 400

    # Validate and sanitize sort and order inputs
    ALLOWED_SORT_COLUMNS = {
        "id",
        "customer",
        "addDate",
        "closeDate",
        "state",
        "shipmentType",
    }
    ALLOWED_ORDER_DIRECTIONS = {"asc", "desc"}
    ALLOWED_STATES = {"open", "closed", "working", "hold"}

    if sort is not None and sort not in ALLOWED_SORT_COLUMNS:
        logging.warning(f"Invalid sort parameter in order_list_get: {sort}")
        return "Invalid sort parameter", 400

    if order is not None and order.lower() not in ALLOWED_ORDER_DIRECTIONS:
        logging.warning(f"Invalid sort parameter in order_list_get: {order}")
        return "Invalid order parameter", 400

    if state is not None and state.lower() not in ALLOWED_STATES:
        logging.warning(f"Invalid state parameter in order_list_get: {state}")
        return "Invalid state parameter", 400

    # Build the WHERE clause dynamically
    query_fields = {}
    if state is not None:
        query_fields["state"] = state

    if customer is not None:
        query_fields["customer"] = customer

    if shipment is not None:
        query_fields["shipmentType"] = shipment

    set_clause = " AND ".join([f"{key} = %s" for key in query_fields.keys()])
    values = list(query_fields.values())

    # Get total items count
    count_query = "SELECT COUNT(*) AS total_orders FROM orders"
    if set_clause:
        count_query += f" WHERE {set_clause}"

    cursor.execute(count_query, values)
    total_items = cursor.fetchone()[0]

    # Build the final query
    query = "SELECT id, customer, addDate, closeDate, products, comment, state, shipmentType FROM orders"
    if set_clause:
        query += f" WHERE {set_clause}"

    if sort and order:
        query += f" ORDER BY {sort} {order.upper()}"

    query += " LIMIT %s OFFSET %s"
    params = values + [limit, offset]

    # Execute the query
    cursor.execute(query, params)
    orders = cursor.fetchall()
    close_db(db)

    # Process the results
    items = []
    for order in orders:
        date_closed = order[3] if order[3] is not None else "-"
        products = json.loads(order[4].replace("'", '"'))

        item = {
            "id": order[0],
            "customer": order[1],
            "dateAdd": order[2],
            "dateClosed": date_closed,
            "comment": order[5],
            "products": products,
            "state": order[6],
            "shipmentType": order[7],
        }
        items.append(item)

    # JSON-Response erstellen
    response = {"items": items, "totalItems": total_items}

    return jsonify(response), 200


@jwt_required()
def orders_info_get():  # noqa: E501
    if not check_auth():
        return "unauthorized", 401

    id = request.args.get("id")

    if check_sql_inject_value(id):
        return "Invalid input", 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders WHERE id = %s", (id,))
    order = cursor.fetchone()

    close_db(db)

    if order is None:
        logging.warning(f"Order {id} not found")
        return "Order not found", 404

    products_str = order[4]

    if order[3] is None:
        dateClosed = "-"
    else:
        dateClosed = order[3]

    order = OrdersResponseItem(
        id=order[0],
        customer=order[1],
        date_add=order[2],
        date_closed=dateClosed,
        comment=order[5],
        products=json.loads(products_str.replace("'", '"')),
        state=order[6],
        shipment_type=order[7],
    )
    return jsonify(order), 200
