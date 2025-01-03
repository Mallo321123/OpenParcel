from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class UserChange(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, first_name=None, last_name=None, email=None, password=None, user_status=None, user_groups=None):  # noqa: E501
        """UserChange - a model defined in OpenAPI

        :param first_name: The first_name of this UserChange.  # noqa: E501
        :type first_name: str
        :param last_name: The last_name of this UserChange.  # noqa: E501
        :type last_name: str
        :param email: The email of this UserChange.  # noqa: E501
        :type email: str
        :param password: The password of this UserChange.  # noqa: E501
        :type password: str
        :param user_status: The user_status of this UserChange.  # noqa: E501
        :type user_status: int
        :param user_groups: The user_groups of this UserChange.  # noqa: E501
        :type user_groups: List[str]
        """
        self.openapi_types = {
            'first_name': str,
            'last_name': str,
            'email': str,
            'password': str,
            'user_status': int,
            'user_groups': List[str]
        }

        self.attribute_map = {
            'first_name': 'firstName',
            'last_name': 'lastName',
            'email': 'email',
            'password': 'password',
            'user_status': 'userStatus',
            'user_groups': 'userGroups'
        }

        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password
        self._user_status = user_status
        self._user_groups = user_groups

    @classmethod
    def from_dict(cls, dikt) -> 'UserChange':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User_change of this UserChange.  # noqa: E501
        :rtype: UserChange
        """
        return util.deserialize_model(dikt, cls)

    @property
    def first_name(self) -> str:
        """Gets the first_name of this UserChange.


        :return: The first_name of this UserChange.
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str):
        """Sets the first_name of this UserChange.


        :param first_name: The first_name of this UserChange.
        :type first_name: str
        """
        if first_name is not None and len(first_name) > 20:
            raise ValueError("Invalid value for `first_name`, length must be less than or equal to `20`")  # noqa: E501

        self._first_name = first_name

    @property
    def last_name(self) -> str:
        """Gets the last_name of this UserChange.


        :return: The last_name of this UserChange.
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str):
        """Sets the last_name of this UserChange.


        :param last_name: The last_name of this UserChange.
        :type last_name: str
        """
        if last_name is not None and len(last_name) > 20:
            raise ValueError("Invalid value for `last_name`, length must be less than or equal to `20`")  # noqa: E501

        self._last_name = last_name

    @property
    def email(self) -> str:
        """Gets the email of this UserChange.


        :return: The email of this UserChange.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this UserChange.


        :param email: The email of this UserChange.
        :type email: str
        """
        if email is not None and len(email) > 100:
            raise ValueError("Invalid value for `email`, length must be less than or equal to `100`")  # noqa: E501

        self._email = email

    @property
    def password(self) -> str:
        """Gets the password of this UserChange.


        :return: The password of this UserChange.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this UserChange.


        :param password: The password of this UserChange.
        :type password: str
        """

        self._password = password

    @property
    def user_status(self) -> int:
        """Gets the user_status of this UserChange.

        User Status  # noqa: E501

        :return: The user_status of this UserChange.
        :rtype: int
        """
        return self._user_status

    @user_status.setter
    def user_status(self, user_status: int):
        """Sets the user_status of this UserChange.

        User Status  # noqa: E501

        :param user_status: The user_status of this UserChange.
        :type user_status: int
        """
        if user_status is not None and user_status > 1:  # noqa: E501
            raise ValueError("Invalid value for `user_status`, must be a value less than or equal to `1`")  # noqa: E501
        if user_status is not None and user_status < 0:  # noqa: E501
            raise ValueError("Invalid value for `user_status`, must be a value greater than or equal to `0`")  # noqa: E501

        self._user_status = user_status

    @property
    def user_groups(self) -> List[str]:
        """Gets the user_groups of this UserChange.


        :return: The user_groups of this UserChange.
        :rtype: List[str]
        """
        return self._user_groups

    @user_groups.setter
    def user_groups(self, user_groups: List[str]):
        """Sets the user_groups of this UserChange.


        :param user_groups: The user_groups of this UserChange.
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
