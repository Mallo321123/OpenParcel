from openapi_server.db import get_db, close_db
from flask_jwt_extended import jwt_required
from openapi_server.security import check_auth

@jwt_required()
def dashboard_get():  # noqa: E501
    if not check_auth():
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT COUNT(*) AS total_done_orders FROM orders WHERE state = 'closed'"
    )
    done = cursor.fetchone()

    cursor.execute(
        "SELECT COUNT(*) AS total_open_orders FROM orders WHERE state = 'open'"
    )
    open = cursor.fetchone()

    cursor.execute(
        "SELECT COUNT(*) AS total_hold_orders FROM orders WHERE state = 'hold'"
    )
    hold = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total_lights FROM lights")
    lights = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total_mappers FROM mapper")
    mappers = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total_products FROM products")
    products = cursor.fetchone()

    close_db(db)

    response = {
        "done": done[0],
        "open": open[0],
        "hold": hold[0],
        "lights": lights[0],
        "mappers": mappers[0],
        "products": products[0],
    }

    return response, 200
