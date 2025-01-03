from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class OrderProducts(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, count=None):  # noqa: E501
        """OrderProducts - a model defined in OpenAPI

        :param id: The id of this OrderProducts.  # noqa: E501
        :type id: int
        :param count: The count of this OrderProducts.  # noqa: E501
        :type count: int
        """
        self.openapi_types = {
            'id': int,
            'count': int
        }

        self.attribute_map = {
            'id': 'id',
            'count': 'count'
        }

        self._id = id
        self._count = count

    @classmethod
    def from_dict(cls, dikt) -> 'OrderProducts':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Order_products of this OrderProducts.  # noqa: E501
        :rtype: OrderProducts
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this OrderProducts.


        :return: The id of this OrderProducts.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this OrderProducts.


        :param id: The id of this OrderProducts.
        :type id: int
        """
        if id is not None and id > 2147483647:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if id is not None and id < 0:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value greater than or equal to `0`")  # noqa: E501

        self._id = id

    @property
    def count(self) -> int:
        """Gets the count of this OrderProducts.


        :return: The count of this OrderProducts.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count: int):
        """Sets the count of this OrderProducts.


        :param count: The count of this OrderProducts.
        :type count: int
        """
        if count is not None and count > 2147483647:  # noqa: E501
            raise ValueError("Invalid value for `count`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if count is not None and count < 0:  # noqa: E501
            raise ValueError("Invalid value for `count`, must be a value greater than or equal to `0`")  # noqa: E501

        self._count = count
