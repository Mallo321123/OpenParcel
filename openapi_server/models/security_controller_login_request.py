from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
import re
from openapi_server import util

import re  # noqa: E501

class SecurityControllerLoginRequest(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, username=None, password=None):  # noqa: E501
        """SecurityControllerLoginRequest - a model defined in OpenAPI

        :param username: The username of this SecurityControllerLoginRequest.  # noqa: E501
        :type username: str
        :param password: The password of this SecurityControllerLoginRequest.  # noqa: E501
        :type password: str
        """
        self.openapi_types = {
            'username': str,
            'password': str
        }

        self.attribute_map = {
            'username': 'username',
            'password': 'password'
        }

        self._username = username
        self._password = password

    @classmethod
    def from_dict(cls, dikt) -> 'SecurityControllerLoginRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The security_controller_login_request of this SecurityControllerLoginRequest.  # noqa: E501
        :rtype: SecurityControllerLoginRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def username(self) -> str:
        """Gets the username of this SecurityControllerLoginRequest.


        :return: The username of this SecurityControllerLoginRequest.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username: str):
        """Sets the username of this SecurityControllerLoginRequest.


        :param username: The username of this SecurityControllerLoginRequest.
        :type username: str
        """
        if username is None:
            raise ValueError("Invalid value for `username`, must not be `None`")  # noqa: E501
        if username is not None and len(username) > 15:
            raise ValueError("Invalid value for `username`, length must be less than or equal to `15`")  # noqa: E501
        if username is not None and not re.search(r'^[0-9a-z]', username):  # noqa: E501
            raise ValueError(r"Invalid value for `username`, must be a follow pattern or equal to `/^[0-9a-z]/`")  # noqa: E501

        self._username = username

    @property
    def password(self) -> str:
        """Gets the password of this SecurityControllerLoginRequest.


        :return: The password of this SecurityControllerLoginRequest.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this SecurityControllerLoginRequest.


        :param password: The password of this SecurityControllerLoginRequest.
        :type password: str
        """
        if password is None:
            raise ValueError("Invalid value for `password`, must not be `None`")  # noqa: E501
        if password is not None and len(password) > 255:
            raise ValueError("Invalid value for `password`, length must be less than or equal to `255`")  # noqa: E501
        if password is not None and not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]$', password):  # noqa: E501
            raise ValueError(r"Invalid value for `password`, must be a follow pattern or equal to `/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]$/`")  # noqa: E501

        self._password = password
