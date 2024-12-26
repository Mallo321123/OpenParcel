import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.orders_add import OrdersAdd  # noqa: E501
from openapi_server import util
from openapi_server.models.orders_response import OrdersResponse
from openapi_server.models.orders_change import OrdersChange

from openapi_server.__init__ import get_db, close_db

import json
import datetime

def orders_delete(id):  # noqa: E501
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE id = %s", (id,))
    result = cursor.fetchone()
    if result is None:
        return "Order not found", 404
    
    cursor.execute("DELETE FROM orders WHERE id = %s", (id,))
    db.commit()
    close_db(db)
    return "Order deleted", 200


def orders_get(limit=None, page=None):  # noqa: E501
    db = get_db()
    cursor = db.cursor()

    offset = limit * page

    cursor.execute("SELECT * FROM orders ORDER BY id DESC LIMIT %s OFFSET %s", (limit, offset))
    orders = cursor.fetchall()
    close_db(db)
    
    for i in range(len(orders)):
        try:
            products = json.loads(orders[i][4])
        except TypeError:
            products = []
            
        orders[i] = OrdersResponse(
            id=orders[i][0],
            customer=orders[i][1],
            dateAdd=orders[i][2],
            dateClose=orders[i][3],
            comment=orders[i][5],
            products=products,
            state=products[i][6],
            shipmentType=products[i][7]
        )
    return orders, 200


def orders_post(orders_add=None):  # noqa: E501
    db = get_db()
    cursor = db.cursor()
    
    if connexion.request.is_json:
        orders_add = OrdersAdd.from_dict(connexion.request.get_json())  # noqa: E501
        
        products_json = json.dumps(orders_add.products)
        
        cursor.execute("""INSERT INTO orders 
                   (customer, addDate, products, comment, state, shipmentType) VALUES (%s, %s, %s, %s, %s, %s)""",
                   (orders_add.customer, datetime.datetime.now(), products_json, orders_add.comment, orders_add.state, orders_add.shipment_type))
        
        db.commit()
        close_db(db)
        return 'Order added', 201
        
    return "invalid request", 400 


def orders_put(id, orders_change=None):  # noqa: E501
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE id = %s", (id,))
    result = cursor.fetchone()
    if result is None:
        return "Order not found", 404
    
    if connexion.request.is_json:
        orders_change = OrdersChange.from_dict(connexion.request.get_json())  # noqa: E501
        
        if isinstance(orders_change, OrdersChange):
            orders_change = orders_change.to_dict()
            
        update_fields = {}
            
        if orders_change.get("dateAdd") is not None:
            update_fields['dateAdd'] = orders_change['dateAdd']
            
        if orders_change.get("state") is not None:
            update_fields['state'] = orders_change['state']
            
        if orders_change.get("shipmentType") is not None:
            update_fields['shipmentType'] = orders_change['shipmentType']
            
        if orders_change.get("comment") is not None:
            update_fields['comment'] = orders_change['comment']
            
        if orders_change.get("products") is not None:
            update_fields['products'] = json.dumps(orders_change['products'])
            
        if orders_change.get("customer") is not None:
            update_fields['customer'] = orders_change['customer']
        
        if orders_change.get("dateClose") is not None:
            update_fields['dateClose'] = orders_change['dateClose']
            
        if update_fields is None:
            return "No fields to update", 400
        
        # Construct the SQL update statement dynamically
        set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
        values = list(update_fields.values())
        values.append(id)

        update_query = f"UPDATE orders SET {set_clause} WHERE id = %s"

        try:
            cursor.execute(update_query, tuple(values))
            db.commit()
        except Exception as e:
            db.rollback()
            return "Failed to update order", 500
        finally:
            close_db(db)
            return "Order updated", 200
        
    return "invalid request", 400
