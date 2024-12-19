from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class Dashboard(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, open=None, done=None, products=None, lights=None, mappers=None):  # noqa: E501
        """Dashboard - a model defined in OpenAPI

        :param open: The open of this Dashboard.  # noqa: E501
        :type open: int
        :param done: The done of this Dashboard.  # noqa: E501
        :type done: int
        :param products: The products of this Dashboard.  # noqa: E501
        :type products: int
        :param lights: The lights of this Dashboard.  # noqa: E501
        :type lights: int
        :param mappers: The mappers of this Dashboard.  # noqa: E501
        :type mappers: int
        """
        self.openapi_types = {
            'open': int,
            'done': int,
            'products': int,
            'lights': int,
            'mappers': int
        }

        self.attribute_map = {
            'open': 'open',
            'done': 'done',
            'products': 'products',
            'lights': 'lights',
            'mappers': 'mappers'
        }

        self._open = open
        self._done = done
        self._products = products
        self._lights = lights
        self._mappers = mappers

    @classmethod
    def from_dict(cls, dikt) -> 'Dashboard':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Dashboard of this Dashboard.  # noqa: E501
        :rtype: Dashboard
        """
        return util.deserialize_model(dikt, cls)

    @property
    def open(self) -> int:
        """Gets the open of this Dashboard.

        count of open orders  # noqa: E501

        :return: The open of this Dashboard.
        :rtype: int
        """
        return self._open

    @open.setter
    def open(self, open: int):
        """Sets the open of this Dashboard.

        count of open orders  # noqa: E501

        :param open: The open of this Dashboard.
        :type open: int
        """

        self._open = open

    @property
    def done(self) -> int:
        """Gets the done of this Dashboard.

        count of completed orders  # noqa: E501

        :return: The done of this Dashboard.
        :rtype: int
        """
        return self._done

    @done.setter
    def done(self, done: int):
        """Sets the done of this Dashboard.

        count of completed orders  # noqa: E501

        :param done: The done of this Dashboard.
        :type done: int
        """

        self._done = done

    @property
    def products(self) -> int:
        """Gets the products of this Dashboard.

        count of avaiable products  # noqa: E501

        :return: The products of this Dashboard.
        :rtype: int
        """
        return self._products

    @products.setter
    def products(self, products: int):
        """Sets the products of this Dashboard.

        count of avaiable products  # noqa: E501

        :param products: The products of this Dashboard.
        :type products: int
        """

        self._products = products

    @property
    def lights(self) -> int:
        """Gets the lights of this Dashboard.


        :return: The lights of this Dashboard.
        :rtype: int
        """
        return self._lights

    @lights.setter
    def lights(self, lights: int):
        """Sets the lights of this Dashboard.


        :param lights: The lights of this Dashboard.
        :type lights: int
        """

        self._lights = lights

    @property
    def mappers(self) -> int:
        """Gets the mappers of this Dashboard.


        :return: The mappers of this Dashboard.
        :rtype: int
        """
        return self._mappers

    @mappers.setter
    def mappers(self, mappers: int):
        """Sets the mappers of this Dashboard.


        :param mappers: The mappers of this Dashboard.
        :type mappers: int
        """

        self._mappers = mappers
