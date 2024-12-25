import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.orders_add import OrdersAdd  # noqa: E501
from openapi_server import util
from openapi_server.models.orders_response import OrdersResponse

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


def orders_put(orders_add=None):  # noqa: E501
    if connexion.request.is_json:
        orders_add = OrdersAdd.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
