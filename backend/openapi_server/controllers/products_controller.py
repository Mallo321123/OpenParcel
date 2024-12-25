import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.products import Products  # noqa: E501
from openapi_server import util

from openapi_server.__init__ import get_db, close_db

import json


def product_add(products=None):  # noqa: E501
    
    db = get_db()
    cursor = db.cursor()
    
    if connexion.request.is_json:
        products = Products.from_dict(connexion.request.get_json())  # noqa: E501
        
        cursor.execute("SELECT * FROM products WHERE name = %s", (products.name,))
        if cursor.fetchone() is not None:
            return "Product already exists", 400
        
        customer_groups_json = json.dumps(products.customer_groups)
        
        try:
            cursor.execute("""INSERT INTO products 
                       (name, comment, customerGroups, difficulty, buildTime) VALUES (%s, %s, %s, %s, %s)""",
                       (products.name, products.comment, customer_groups_json, products.difficulty, products.build_time))
        
        except Exception as e:
            return str(e), 400
        
        db.commit()
        close_db(db)
        
        return "Product created", 200


def products_delete(id):  # noqa: E501
    """delete a product

    deletes a product # noqa: E501

    :param id: The product that needs to be deleted
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def products_list(limit=None, page=None):  # noqa: E501
    """list of products

    lists all avaiable products # noqa: E501

    :param limit: items per page
    :type limit: int
    :param page: page number
    :type page: int

    :rtype: Union[List[Products], Tuple[List[Products], int], Tuple[List[Products], int, Dict[str, str]]
    """
    return 'do some magic!'


def update_product(products=None):  # noqa: E501
    """update product

    updates product properties # noqa: E501

    :param products: 
    :type products: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        products = Products.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
