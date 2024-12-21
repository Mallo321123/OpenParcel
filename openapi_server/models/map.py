from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
import re
from openapi_server import util

import re  # noqa: E501

class Map(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None, product_id=None, light_id=None):  # noqa: E501
        """Map - a model defined in OpenAPI

        :param id: The id of this Map.  # noqa: E501
        :type id: int
        :param name: The name of this Map.  # noqa: E501
        :type name: str
        :param product_id: The product_id of this Map.  # noqa: E501
        :type product_id: List[int]
        :param light_id: The light_id of this Map.  # noqa: E501
        :type light_id: List[int]
        """
        self.openapi_types = {
            'id': int,
            'name': str,
            'product_id': List[int],
            'light_id': List[int]
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'product_id': 'productId',
            'light_id': 'lightId'
        }

        self._id = id
        self._name = name
        self._product_id = product_id
        self._light_id = light_id

    @classmethod
    def from_dict(cls, dikt) -> 'Map':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Map of this Map.  # noqa: E501
        :rtype: Map
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Map.


        :return: The id of this Map.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Map.


        :param id: The id of this Map.
        :type id: int
        """
        if id is not None and id > 2147483647:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if id is not None and id < 0:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value greater than or equal to `0`")  # noqa: E501

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this Map.


        :return: The name of this Map.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Map.


        :param name: The name of this Map.
        :type name: str
        """
        if name is not None and len(name) > 255:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `255`")  # noqa: E501
        if name is not None and not re.search(r'^example-[0-9a-z]', name):  # noqa: E501
            raise ValueError(r"Invalid value for `name`, must be a follow pattern or equal to `/^example-[0-9a-z]/`")  # noqa: E501

        self._name = name

    @property
    def product_id(self) -> List[int]:
        """Gets the product_id of this Map.


        :return: The product_id of this Map.
        :rtype: List[int]
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id: List[int]):
        """Sets the product_id of this Map.


        :param product_id: The product_id of this Map.
        :type product_id: List[int]
        """
        if product_id is not None and len(product_id) > 100:
            raise ValueError("Invalid value for `product_id`, number of items must be less than or equal to `100`")  # noqa: E501

        self._product_id = product_id

    @property
    def light_id(self) -> List[int]:
        """Gets the light_id of this Map.


        :return: The light_id of this Map.
        :rtype: List[int]
        """
        return self._light_id

    @light_id.setter
    def light_id(self, light_id: List[int]):
        """Sets the light_id of this Map.


        :param light_id: The light_id of this Map.
        :type light_id: List[int]
        """
        if light_id is not None and len(light_id) > 100:
            raise ValueError("Invalid value for `light_id`, number of items must be less than or equal to `100`")  # noqa: E501

        self._light_id = light_id
