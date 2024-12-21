import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.products import Products  # noqa: E501
from openapi_server import util


def product_add(products=None):  # noqa: E501
    """add a product

    adds a product # noqa: E501

    :param products: 
    :type products: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        products = Products.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def products_delete(id):  # noqa: E501
    """delete a product

    deletes a product # noqa: E501

    :param id: The product that needs to be deleted
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def products_list():  # noqa: E501
    """list of products

    lists all avaiable products # noqa: E501


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
