from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.order_products import OrderProducts
import re
from openapi_server import util

from openapi_server.models.order_products import OrderProducts  # noqa: E501
import re  # noqa: E501

class OrdersResponseItem(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, customer=None, products=None, state=None, date_add=None, date_closed=None, comment=None, shipment_type=None):  # noqa: E501
        """OrdersResponseItem - a model defined in OpenAPI

        :param id: The id of this OrdersResponseItem.  # noqa: E501
        :type id: int
        :param customer: The customer of this OrdersResponseItem.  # noqa: E501
        :type customer: str
        :param products: The products of this OrdersResponseItem.  # noqa: E501
        :type products: List[OrderProducts]
        :param state: The state of this OrdersResponseItem.  # noqa: E501
        :type state: str
        :param date_add: The date_add of this OrdersResponseItem.  # noqa: E501
        :type date_add: str
        :param date_closed: The date_closed of this OrdersResponseItem.  # noqa: E501
        :type date_closed: str
        :param comment: The comment of this OrdersResponseItem.  # noqa: E501
        :type comment: str
        :param shipment_type: The shipment_type of this OrdersResponseItem.  # noqa: E501
        :type shipment_type: str
        """
        self.openapi_types = {
            'id': int,
            'customer': str,
            'products': List[OrderProducts],
            'state': str,
            'date_add': str,
            'date_closed': str,
            'comment': str,
            'shipment_type': str
        }

        self.attribute_map = {
            'id': 'id',
            'customer': 'customer',
            'products': 'products',
            'state': 'state',
            'date_add': 'dateAdd',
            'date_closed': 'dateClosed',
            'comment': 'comment',
            'shipment_type': 'shipmentType'
        }

        self._id = id
        self._customer = customer
        self._products = products
        self._state = state
        self._date_add = date_add
        self._date_closed = date_closed
        self._comment = comment
        self._shipment_type = shipment_type

    @classmethod
    def from_dict(cls, dikt) -> 'OrdersResponseItem':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Orders_response_item of this OrdersResponseItem.  # noqa: E501
        :rtype: OrdersResponseItem
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this OrdersResponseItem.


        :return: The id of this OrdersResponseItem.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this OrdersResponseItem.


        :param id: The id of this OrdersResponseItem.
        :type id: int
        """
        if id is not None and id > 2147483647:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if id is not None and id < 0:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value greater than or equal to `0`")  # noqa: E501

        self._id = id

    @property
    def customer(self) -> str:
        """Gets the customer of this OrdersResponseItem.


        :return: The customer of this OrdersResponseItem.
        :rtype: str
        """
        return self._customer

    @customer.setter
    def customer(self, customer: str):
        """Sets the customer of this OrdersResponseItem.


        :param customer: The customer of this OrdersResponseItem.
        :type customer: str
        """
        if customer is not None and len(customer) > 255:
            raise ValueError("Invalid value for `customer`, length must be less than or equal to `255`")  # noqa: E501

        self._customer = customer

    @property
    def products(self) -> List[OrderProducts]:
        """Gets the products of this OrdersResponseItem.


        :return: The products of this OrdersResponseItem.
        :rtype: List[OrderProducts]
        """
        return self._products

    @products.setter
    def products(self, products: List[OrderProducts]):
        """Sets the products of this OrdersResponseItem.


        :param products: The products of this OrdersResponseItem.
        :type products: List[OrderProducts]
        """
        if products is not None and len(products) > 255:
            raise ValueError("Invalid value for `products`, number of items must be less than or equal to `255`")  # noqa: E501

        self._products = products

    @property
    def state(self) -> str:
        """Gets the state of this OrdersResponseItem.


        :return: The state of this OrdersResponseItem.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state: str):
        """Sets the state of this OrdersResponseItem.


        :param state: The state of this OrdersResponseItem.
        :type state: str
        """
        allowed_values = ["open", "working", "hold", "closed"]  # noqa: E501
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}"
                .format(state, allowed_values)
            )

        self._state = state

    @property
    def date_add(self) -> str:
        """Gets the date_add of this OrdersResponseItem.


        :return: The date_add of this OrdersResponseItem.
        :rtype: str
        """
        return self._date_add

    @date_add.setter
    def date_add(self, date_add: str):
        """Sets the date_add of this OrdersResponseItem.


        :param date_add: The date_add of this OrdersResponseItem.
        :type date_add: str
        """
        if date_add is not None and len(date_add) > 255:
            raise ValueError("Invalid value for `date_add`, length must be less than or equal to `255`")  # noqa: E501

        self._date_add = date_add

    @property
    def date_closed(self) -> str:
        """Gets the date_closed of this OrdersResponseItem.


        :return: The date_closed of this OrdersResponseItem.
        :rtype: str
        """
        return self._date_closed

    @date_closed.setter
    def date_closed(self, date_closed: str):
        """Sets the date_closed of this OrdersResponseItem.


        :param date_closed: The date_closed of this OrdersResponseItem.
        :type date_closed: str
        """
        if date_closed is not None and len(date_closed) > 255:
            raise ValueError("Invalid value for `date_closed`, length must be less than or equal to `255`")  # noqa: E501

        self._date_closed = date_closed

    @property
    def comment(self) -> str:
        """Gets the comment of this OrdersResponseItem.


        :return: The comment of this OrdersResponseItem.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment: str):
        """Sets the comment of this OrdersResponseItem.


        :param comment: The comment of this OrdersResponseItem.
        :type comment: str
        """
        if comment is not None and len(comment) > 255:
            raise ValueError("Invalid value for `comment`, length must be less than or equal to `255`")  # noqa: E501
        if comment is not None and not re.search(r'^.*$', comment):  # noqa: E501
            raise ValueError(r"Invalid value for `comment`, must be a follow pattern or equal to `/^.*$/`")  # noqa: E501

        self._comment = comment

    @property
    def shipment_type(self) -> str:
        """Gets the shipment_type of this OrdersResponseItem.


        :return: The shipment_type of this OrdersResponseItem.
        :rtype: str
        """
        return self._shipment_type

    @shipment_type.setter
    def shipment_type(self, shipment_type: str):
        """Sets the shipment_type of this OrdersResponseItem.


        :param shipment_type: The shipment_type of this OrdersResponseItem.
        :type shipment_type: str
        """
        if shipment_type is not None and len(shipment_type) > 255:
            raise ValueError("Invalid value for `shipment_type`, length must be less than or equal to `255`")  # noqa: E501
        if shipment_type is not None and not re.search(r'^[0-9a-zA-Z]+$', shipment_type):  # noqa: E501
            raise ValueError(r"Invalid value for `shipment_type`, must be a follow pattern or equal to `/^[0-9a-zA-Z]+$/`")  # noqa: E501

        self._shipment_type = shipment_type
