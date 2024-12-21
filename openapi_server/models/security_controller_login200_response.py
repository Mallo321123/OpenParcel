from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
import re
from openapi_server import util

import re  # noqa: E501

class SecurityControllerLogin200Response(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, message=None, success=None, token=None):  # noqa: E501
        """SecurityControllerLogin200Response - a model defined in OpenAPI

        :param message: The message of this SecurityControllerLogin200Response.  # noqa: E501
        :type message: str
        :param success: The success of this SecurityControllerLogin200Response.  # noqa: E501
        :type success: bool
        :param token: The token of this SecurityControllerLogin200Response.  # noqa: E501
        :type token: str
        """
        self.openapi_types = {
            'message': str,
            'success': bool,
            'token': str
        }

        self.attribute_map = {
            'message': 'message',
            'success': 'success',
            'token': 'token'
        }

        self._message = message
        self._success = success
        self._token = token

    @classmethod
    def from_dict(cls, dikt) -> 'SecurityControllerLogin200Response':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The security_controller_login_200_response of this SecurityControllerLogin200Response.  # noqa: E501
        :rtype: SecurityControllerLogin200Response
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message(self) -> str:
        """Gets the message of this SecurityControllerLogin200Response.


        :return: The message of this SecurityControllerLogin200Response.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this SecurityControllerLogin200Response.


        :param message: The message of this SecurityControllerLogin200Response.
        :type message: str
        """

        self._message = message

    @property
    def success(self) -> bool:
        """Gets the success of this SecurityControllerLogin200Response.


        :return: The success of this SecurityControllerLogin200Response.
        :rtype: bool
        """
        return self._success

    @success.setter
    def success(self, success: bool):
        """Sets the success of this SecurityControllerLogin200Response.


        :param success: The success of this SecurityControllerLogin200Response.
        :type success: bool
        """

        self._success = success

    @property
    def token(self) -> str:
        """Gets the token of this SecurityControllerLogin200Response.


        :return: The token of this SecurityControllerLogin200Response.
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token: str):
        """Sets the token of this SecurityControllerLogin200Response.


        :param token: The token of this SecurityControllerLogin200Response.
        :type token: str
        """
        if token is not None and len(token) > 255:
            raise ValueError("Invalid value for `token`, length must be less than or equal to `255`")  # noqa: E501
        if token is not None and not re.search(r'^[\w-]*\.[\w-]*\.[\w-]*$', token):  # noqa: E501
            raise ValueError(r"Invalid value for `token`, must be a follow pattern or equal to `/^[\w-]*\.[\w-]*\.[\w-]*$/`")  # noqa: E501

        self._token = token
