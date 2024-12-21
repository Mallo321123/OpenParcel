from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.products import Products
import re
from openapi_server import util

from openapi_server.models.products import Products  # noqa: E501
import re  # noqa: E501

class Orders(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, customer=None, products=None, state=None, date_add=None, date_closed=None):  # noqa: E501
        """Orders - a model defined in OpenAPI

        :param id: The id of this Orders.  # noqa: E501
        :type id: int
        :param customer: The customer of this Orders.  # noqa: E501
        :type customer: str
        :param products: The products of this Orders.  # noqa: E501
        :type products: List[Products]
        :param state: The state of this Orders.  # noqa: E501
        :type state: str
        :param date_add: The date_add of this Orders.  # noqa: E501
        :type date_add: str
        :param date_closed: The date_closed of this Orders.  # noqa: E501
        :type date_closed: str
        """
        self.openapi_types = {
            'id': int,
            'customer': str,
            'products': List[Products],
            'state': str,
            'date_add': str,
            'date_closed': str
        }

        self.attribute_map = {
            'id': 'id',
            'customer': 'customer',
            'products': 'products',
            'state': 'state',
            'date_add': 'dateAdd',
            'date_closed': 'dateClosed'
        }

        self._id = id
        self._customer = customer
        self._products = products
        self._state = state
        self._date_add = date_add
        self._date_closed = date_closed

    @classmethod
    def from_dict(cls, dikt) -> 'Orders':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Orders of this Orders.  # noqa: E501
        :rtype: Orders
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Orders.


        :return: The id of this Orders.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Orders.


        :param id: The id of this Orders.
        :type id: int
        """
        if id is not None and id > 2147483647:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if id is not None and id < 0:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value greater than or equal to `0`")  # noqa: E501

        self._id = id

    @property
    def customer(self) -> str:
        """Gets the customer of this Orders.


        :return: The customer of this Orders.
        :rtype: str
        """
        return self._customer

    @customer.setter
    def customer(self, customer: str):
        """Sets the customer of this Orders.


        :param customer: The customer of this Orders.
        :type customer: str
        """
        if customer is not None and len(customer) > 255:
            raise ValueError("Invalid value for `customer`, length must be less than or equal to `255`")  # noqa: E501
        if customer is not None and not re.search(r'^example-[0-9a-z]+$^example-[0-9a-z]+$^example-[0-9a-z]+$', customer):  # noqa: E501
            raise ValueError(r"Invalid value for `customer`, must be a follow pattern or equal to `/^example-[0-9a-z]+$^example-[0-9a-z]+$^example-[0-9a-z]+$/`")  # noqa: E501

        self._customer = customer

    @property
    def products(self) -> List[Products]:
        """Gets the products of this Orders.


        :return: The products of this Orders.
        :rtype: List[Products]
        """
        return self._products

    @products.setter
    def products(self, products: List[Products]):
        """Sets the products of this Orders.


        :param products: The products of this Orders.
        :type products: List[Products]
        """
        if products is not None and len(products) > 100:
            raise ValueError("Invalid value for `products`, number of items must be less than or equal to `100`")  # noqa: E501

        self._products = products

    @property
    def state(self) -> str:
        """Gets the state of this Orders.


        :return: The state of this Orders.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state: str):
        """Sets the state of this Orders.


        :param state: The state of this Orders.
        :type state: str
        """
        allowed_values = ["open", "in work", "hold", "closed"]  # noqa: E501
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}"
                .format(state, allowed_values)
            )

        self._state = state

    @property
    def date_add(self) -> str:
        """Gets the date_add of this Orders.


        :return: The date_add of this Orders.
        :rtype: str
        """
        return self._date_add

    @date_add.setter
    def date_add(self, date_add: str):
        """Sets the date_add of this Orders.


        :param date_add: The date_add of this Orders.
        :type date_add: str
        """
        if date_add is not None and len(date_add) > 30:
            raise ValueError("Invalid value for `date_add`, length must be less than or equal to `30`")  # noqa: E501
        if date_add is not None and not re.search(r'^example-[0-9a-z]+$^example-[0-9a-z]+$^example-[0-9a-z]+$', date_add):  # noqa: E501
            raise ValueError(r"Invalid value for `date_add`, must be a follow pattern or equal to `/^example-[0-9a-z]+$^example-[0-9a-z]+$^example-[0-9a-z]+$/`")  # noqa: E501

        self._date_add = date_add

    @property
    def date_closed(self) -> str:
        """Gets the date_closed of this Orders.


        :return: The date_closed of this Orders.
        :rtype: str
        """
        return self._date_closed

    @date_closed.setter
    def date_closed(self, date_closed: str):
        """Sets the date_closed of this Orders.


        :param date_closed: The date_closed of this Orders.
        :type date_closed: str
        """
        if date_closed is not None and len(date_closed) > 30:
            raise ValueError("Invalid value for `date_closed`, length must be less than or equal to `30`")  # noqa: E501
        if date_closed is not None and not re.search(r'^example-[0-9a-z]+$^example-[0-9a-z]+$^example-[0-9a-z]+$', date_closed):  # noqa: E501
            raise ValueError(r"Invalid value for `date_closed`, must be a follow pattern or equal to `/^example-[0-9a-z]+$^example-[0-9a-z]+$^example-[0-9a-z]+$/`")  # noqa: E501

        self._date_closed = date_closed