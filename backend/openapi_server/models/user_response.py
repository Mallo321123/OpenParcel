from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class UserResponse(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, username=None, first_name=None, last_name=None, email=None, user_status=None, user_groups=None):  # noqa: E501
        """UserResponse - a model defined in OpenAPI

        :param id: The id of this UserResponse.  # noqa: E501
        :type id: int
        :param username: The username of this UserResponse.  # noqa: E501
        :type username: str
        :param first_name: The first_name of this UserResponse.  # noqa: E501
        :type first_name: str
        :param last_name: The last_name of this UserResponse.  # noqa: E501
        :type last_name: str
        :param email: The email of this UserResponse.  # noqa: E501
        :type email: str
        :param user_status: The user_status of this UserResponse.  # noqa: E501
        :type user_status: int
        :param user_groups: The user_groups of this UserResponse.  # noqa: E501
        :type user_groups: List[str]
        """
        self.openapi_types = {
            'id': int,
            'username': str,
            'first_name': str,
            'last_name': str,
            'email': str,
            'user_status': int,
            'user_groups': List[str]
        }

        self.attribute_map = {
            'id': 'id',
            'username': 'username',
            'first_name': 'firstName',
            'last_name': 'lastName',
            'email': 'email',
            'user_status': 'userStatus',
            'user_groups': 'userGroups'
        }

        self._id = id
        self._username = username
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._user_status = user_status
        self._user_groups = user_groups

    @classmethod
    def from_dict(cls, dikt) -> 'UserResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User_response of this UserResponse.  # noqa: E501
        :rtype: UserResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this UserResponse.


        :return: The id of this UserResponse.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this UserResponse.


        :param id: The id of this UserResponse.
        :type id: int
        """
        if id is not None and id > 2147483647:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if id is not None and id < 0:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value greater than or equal to `0`")  # noqa: E501

        self._id = id

    @property
    def username(self) -> str:
        """Gets the username of this UserResponse.


        :return: The username of this UserResponse.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username: str):
        """Sets the username of this UserResponse.


        :param username: The username of this UserResponse.
        :type username: str
        """
        if username is not None and len(username) > 15:
            raise ValueError("Invalid value for `username`, length must be less than or equal to `15`")  # noqa: E501

        self._username = username

    @property
    def first_name(self) -> str:
        """Gets the first_name of this UserResponse.


        :return: The first_name of this UserResponse.
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str):
        """Sets the first_name of this UserResponse.


        :param first_name: The first_name of this UserResponse.
        :type first_name: str
        """
        if first_name is not None and len(first_name) > 20:
            raise ValueError("Invalid value for `first_name`, length must be less than or equal to `20`")  # noqa: E501

        self._first_name = first_name

    @property
    def last_name(self) -> str:
        """Gets the last_name of this UserResponse.


        :return: The last_name of this UserResponse.
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str):
        """Sets the last_name of this UserResponse.


        :param last_name: The last_name of this UserResponse.
        :type last_name: str
        """
        if last_name is not None and len(last_name) > 20:
            raise ValueError("Invalid value for `last_name`, length must be less than or equal to `20`")  # noqa: E501

        self._last_name = last_name

    @property
    def email(self) -> str:
        """Gets the email of this UserResponse.


        :return: The email of this UserResponse.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this UserResponse.


        :param email: The email of this UserResponse.
        :type email: str
        """
        if email is not None and len(email) > 100:
            raise ValueError("Invalid value for `email`, length must be less than or equal to `100`")  # noqa: E501

        self._email = email

    @property
    def user_status(self) -> int:
        """Gets the user_status of this UserResponse.

        User Status  # noqa: E501

        :return: The user_status of this UserResponse.
        :rtype: int
        """
        return self._user_status

    @user_status.setter
    def user_status(self, user_status: int):
        """Sets the user_status of this UserResponse.

        User Status  # noqa: E501

        :param user_status: The user_status of this UserResponse.
        :type user_status: int
        """

        self._user_status = user_status

    @property
    def user_groups(self) -> List[str]:
        """Gets the user_groups of this UserResponse.


        :return: The user_groups of this UserResponse.
        :rtype: List[str]
        """
        return self._user_groups

    @user_groups.setter
    def user_groups(self, user_groups: List[str]):
        """Sets the user_groups of this UserResponse.


        :param user_groups: The user_groups of this UserResponse.
        :type user_groups: List[str]
        """
        allowed_values = ["admin", "products", "lights", "settings", "orders"]  # noqa: E501
        if not set(user_groups).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `user_groups` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(user_groups) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._user_groups = user_groups
