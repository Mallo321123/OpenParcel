import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.orders import Orders  # noqa: E501
from openapi_server import util


def orders_delete(id):  # noqa: E501
    """delete a order

    deletes a order # noqa: E501

    :param id: The order that needs to be deleted
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def orders_get():  # noqa: E501
    """list all orders

    lists all orders # noqa: E501


    :rtype: Union[List[Orders], Tuple[List[Orders], int], Tuple[List[Orders], int, Dict[str, str]]
    """
    return 'do some magic!'


def orders_post(orders=None):  # noqa: E501
    """add an order

    adds an order # noqa: E501

    :param orders: 
    :type orders: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        orders = Orders.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def orders_put(orders=None):  # noqa: E501
    """update an order

    updates an order # noqa: E501

    :param orders: 
    :type orders: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        orders = Orders.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
