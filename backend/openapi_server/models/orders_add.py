from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
import re
from openapi_server import util

import re  # noqa: E501

class OrdersAdd(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, customer=None, products=None, state=None, comment=None, shipment_type=None):  # noqa: E501
        """OrdersAdd - a model defined in OpenAPI

        :param customer: The customer of this OrdersAdd.  # noqa: E501
        :type customer: str
        :param products: The products of this OrdersAdd.  # noqa: E501
        :type products: List[int]
        :param state: The state of this OrdersAdd.  # noqa: E501
        :type state: str
        :param comment: The comment of this OrdersAdd.  # noqa: E501
        :type comment: str
        :param shipment_type: The shipment_type of this OrdersAdd.  # noqa: E501
        :type shipment_type: str
        """
        self.openapi_types = {
            'customer': str,
            'products': List[int],
            'state': str,
            'comment': str,
            'shipment_type': str
        }

        self.attribute_map = {
            'customer': 'customer',
            'products': 'products',
            'state': 'state',
            'comment': 'comment',
            'shipment_type': 'shipmentType'
        }

        self._customer = customer
        self._products = products
        self._state = state
        self._comment = comment
        self._shipment_type = shipment_type

    @classmethod
    def from_dict(cls, dikt) -> 'OrdersAdd':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Orders_add of this OrdersAdd.  # noqa: E501
        :rtype: OrdersAdd
        """
        return util.deserialize_model(dikt, cls)

    @property
    def customer(self) -> str:
        """Gets the customer of this OrdersAdd.


        :return: The customer of this OrdersAdd.
        :rtype: str
        """
        return self._customer

    @customer.setter
    def customer(self, customer: str):
        """Sets the customer of this OrdersAdd.


        :param customer: The customer of this OrdersAdd.
        :type customer: str
        """
        if customer is not None and len(customer) > 255:
            raise ValueError("Invalid value for `customer`, length must be less than or equal to `255`")  # noqa: E501
        if customer is not None and not re.search(r'^[A-ZÄÖÜa-zäöüß]+(?:[-\' ][A-ZÄÖÜa-zäöüß]+)+$', customer):  # noqa: E501
            raise ValueError(r"Invalid value for `customer`, must be a follow pattern or equal to `/^[A-ZÄÖÜa-zäöüß]+(?:[-' ][A-ZÄÖÜa-zäöüß]+)+$/`")  # noqa: E501

        self._customer = customer

    @property
    def products(self) -> List[int]:
        """Gets the products of this OrdersAdd.


        :return: The products of this OrdersAdd.
        :rtype: List[int]
        """
        return self._products

    @products.setter
    def products(self, products: List[int]):
        """Sets the products of this OrdersAdd.


        :param products: The products of this OrdersAdd.
        :type products: List[int]
        """
        if products is not None and len(products) > 255:
            raise ValueError("Invalid value for `products`, number of items must be less than or equal to `255`")  # noqa: E501

        self._products = products

    @property
    def state(self) -> str:
        """Gets the state of this OrdersAdd.


        :return: The state of this OrdersAdd.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state: str):
        """Sets the state of this OrdersAdd.


        :param state: The state of this OrdersAdd.
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
    def comment(self) -> str:
        """Gets the comment of this OrdersAdd.


        :return: The comment of this OrdersAdd.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment: str):
        """Sets the comment of this OrdersAdd.


        :param comment: The comment of this OrdersAdd.
        :type comment: str
        """
        if comment is not None and len(comment) > 255:
            raise ValueError("Invalid value for `comment`, length must be less than or equal to `255`")  # noqa: E501
        if comment is not None and not re.search(r'^.*$', comment):  # noqa: E501
            raise ValueError(r"Invalid value for `comment`, must be a follow pattern or equal to `/^.*$/`")  # noqa: E501

        self._comment = comment

    @property
    def shipment_type(self) -> str:
        """Gets the shipment_type of this OrdersAdd.


        :return: The shipment_type of this OrdersAdd.
        :rtype: str
        """
        return self._shipment_type

    @shipment_type.setter
    def shipment_type(self, shipment_type: str):
        """Sets the shipment_type of this OrdersAdd.


        :param shipment_type: The shipment_type of this OrdersAdd.
        :type shipment_type: str
        """
        if shipment_type is not None and len(shipment_type) > 255:
            raise ValueError("Invalid value for `shipment_type`, length must be less than or equal to `255`")  # noqa: E501
        if shipment_type is not None and not re.search(r'^[0-9a-zA-Z]+$', shipment_type):  # noqa: E501
            raise ValueError(r"Invalid value for `shipment_type`, must be a follow pattern or equal to `/^[0-9a-zA-Z]+$/`")  # noqa: E501

        self._shipment_type = shipment_type