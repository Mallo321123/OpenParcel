import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.orders_add import OrdersAdd  # noqa: E501
from openapi_server import util


def orders_delete(id):  # noqa: E501
    """delete a order

    deletes a order # noqa: E501

    :param id: The order that needs to be deleted
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def orders_get(limit=None, page=None):  # noqa: E501
    """list all orders

    lists all orders # noqa: E501

    :param limit: items per page
    :type limit: int
    :param page: page number
    :type page: int

    :rtype: Union[List[OrdersAdd], Tuple[List[OrdersAdd], int], Tuple[List[OrdersAdd], int, Dict[str, str]]
    """
    return 'do some magic!'


def orders_post(orders_add=None):  # noqa: E501
    """add an order

    adds an order # noqa: E501

    :param orders_add: 
    :type orders_add: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        orders_add = OrdersAdd.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def orders_put(orders_add=None):  # noqa: E501
    """update an order

    updates an order # noqa: E501

    :param orders_add: 
    :type orders_add: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        orders_add = OrdersAdd.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
