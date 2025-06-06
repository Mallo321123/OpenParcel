from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class Products(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None, comment=None, difficulty=None, build_time=None, customer_groups=None):  # noqa: E501
        """Products - a model defined in OpenAPI

        :param name: The name of this Products.  # noqa: E501
        :type name: str
        :param comment: The comment of this Products.  # noqa: E501
        :type comment: str
        :param difficulty: The difficulty of this Products.  # noqa: E501
        :type difficulty: int
        :param build_time: The build_time of this Products.  # noqa: E501
        :type build_time: str
        :param customer_groups: The customer_groups of this Products.  # noqa: E501
        :type customer_groups: List[str]
        """
        self.openapi_types = {
            'name': str,
            'comment': str,
            'difficulty': int,
            'build_time': str,
            'customer_groups': List[str]
        }

        self.attribute_map = {
            'name': 'name',
            'comment': 'comment',
            'difficulty': 'difficulty',
            'build_time': 'buildTime',
            'customer_groups': 'customerGroups'
        }

        self._name = name
        self._comment = comment
        self._difficulty = difficulty
        self._build_time = build_time
        self._customer_groups = customer_groups

    @classmethod
    def from_dict(cls, dikt) -> 'Products':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Products of this Products.  # noqa: E501
        :rtype: Products
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Products.


        :return: The name of this Products.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Products.


        :param name: The name of this Products.
        :type name: str
        """
        if name is not None and len(name) > 255:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `255`")  # noqa: E501

        self._name = name

    @property
    def comment(self) -> str:
        """Gets the comment of this Products.


        :return: The comment of this Products.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment: str):
        """Sets the comment of this Products.


        :param comment: The comment of this Products.
        :type comment: str
        """
        if comment is not None and len(comment) > 65535:
            raise ValueError("Invalid value for `comment`, length must be less than or equal to `65535`")  # noqa: E501

        self._comment = comment

    @property
    def difficulty(self) -> int:
        """Gets the difficulty of this Products.


        :return: The difficulty of this Products.
        :rtype: int
        """
        return self._difficulty

    @difficulty.setter
    def difficulty(self, difficulty: int):
        """Sets the difficulty of this Products.


        :param difficulty: The difficulty of this Products.
        :type difficulty: int
        """
        allowed_values = [1, 2, 3, 4, 5]  # noqa: E501
        if difficulty not in allowed_values:
            raise ValueError(
                "Invalid value for `difficulty` ({0}), must be one of {1}"
                .format(difficulty, allowed_values)
            )

        self._difficulty = difficulty

    @property
    def build_time(self) -> str:
        """Gets the build_time of this Products.


        :return: The build_time of this Products.
        :rtype: str
        """
        return self._build_time

    @build_time.setter
    def build_time(self, build_time: str):
        """Sets the build_time of this Products.


        :param build_time: The build_time of this Products.
        :type build_time: str
        """
        if build_time is not None and len(build_time) > 255:
            raise ValueError("Invalid value for `build_time`, length must be less than or equal to `255`")  # noqa: E501

        self._build_time = build_time

    @property
    def customer_groups(self) -> List[str]:
        """Gets the customer_groups of this Products.


        :return: The customer_groups of this Products.
        :rtype: List[str]
        """
        return self._customer_groups

    @customer_groups.setter
    def customer_groups(self, customer_groups: List[str]):
        """Sets the customer_groups of this Products.


        :param customer_groups: The customer_groups of this Products.
        :type customer_groups: List[str]
        """
        if customer_groups is not None and len(customer_groups) > 100:
            raise ValueError("Invalid value for `customer_groups`, number of items must be less than or equal to `100`")  # noqa: E501

        self._customer_groups = customer_groups
