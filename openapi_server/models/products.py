from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class Products(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None, comment=None, difficulty=None, build_time=None, customer_groups=None):  # noqa: E501
        """Products - a model defined in OpenAPI

        :param id: The id of this Products.  # noqa: E501
        :type id: int
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
            'id': int,
            'name': str,
            'comment': str,
            'difficulty': int,
            'build_time': str,
            'customer_groups': List[str]
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'comment': 'comment',
            'difficulty': 'difficulty',
            'build_time': 'buildTime',
            'customer_groups': 'customerGroups'
        }

        self._id = id
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
    def id(self) -> int:
        """Gets the id of this Products.


        :return: The id of this Products.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Products.


        :param id: The id of this Products.
        :type id: int
        """

        self._id = id

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

        self._customer_groups = customer_groups
