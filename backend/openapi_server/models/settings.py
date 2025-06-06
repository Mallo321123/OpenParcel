from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class Settings(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, min_password_length=None, token_expiration=None, max_login_tries=None, block_time=None):  # noqa: E501
        """Settings - a model defined in OpenAPI

        :param min_password_length: The min_password_length of this Settings.  # noqa: E501
        :type min_password_length: int
        :param token_expiration: The token_expiration of this Settings.  # noqa: E501
        :type token_expiration: int
        :param max_login_tries: The max_login_tries of this Settings.  # noqa: E501
        :type max_login_tries: int
        :param block_time: The block_time of this Settings.  # noqa: E501
        :type block_time: int
        """
        self.openapi_types = {
            'min_password_length': int,
            'token_expiration': int,
            'max_login_tries': int,
            'block_time': int
        }

        self.attribute_map = {
            'min_password_length': 'minPasswordLength',
            'token_expiration': 'tokenExpiration',
            'max_login_tries': 'maxLoginTries',
            'block_time': 'blockTime'
        }

        self._min_password_length = min_password_length
        self._token_expiration = token_expiration
        self._max_login_tries = max_login_tries
        self._block_time = block_time

    @classmethod
    def from_dict(cls, dikt) -> 'Settings':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Settings of this Settings.  # noqa: E501
        :rtype: Settings
        """
        return util.deserialize_model(dikt, cls)

    @property
    def min_password_length(self) -> int:
        """Gets the min_password_length of this Settings.


        :return: The min_password_length of this Settings.
        :rtype: int
        """
        return self._min_password_length

    @min_password_length.setter
    def min_password_length(self, min_password_length: int):
        """Sets the min_password_length of this Settings.


        :param min_password_length: The min_password_length of this Settings.
        :type min_password_length: int
        """
        if min_password_length is not None and min_password_length > 1024:  # noqa: E501
            raise ValueError("Invalid value for `min_password_length`, must be a value less than or equal to `1024`")  # noqa: E501
        if min_password_length is not None and min_password_length < 0:  # noqa: E501
            raise ValueError("Invalid value for `min_password_length`, must be a value greater than or equal to `0`")  # noqa: E501

        self._min_password_length = min_password_length

    @property
    def token_expiration(self) -> int:
        """Gets the token_expiration of this Settings.


        :return: The token_expiration of this Settings.
        :rtype: int
        """
        return self._token_expiration

    @token_expiration.setter
    def token_expiration(self, token_expiration: int):
        """Sets the token_expiration of this Settings.


        :param token_expiration: The token_expiration of this Settings.
        :type token_expiration: int
        """
        if token_expiration is not None and token_expiration > 2147483647:  # noqa: E501
            raise ValueError("Invalid value for `token_expiration`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if token_expiration is not None and token_expiration < 0:  # noqa: E501
            raise ValueError("Invalid value for `token_expiration`, must be a value greater than or equal to `0`")  # noqa: E501

        self._token_expiration = token_expiration

    @property
    def max_login_tries(self) -> int:
        """Gets the max_login_tries of this Settings.


        :return: The max_login_tries of this Settings.
        :rtype: int
        """
        return self._max_login_tries

    @max_login_tries.setter
    def max_login_tries(self, max_login_tries: int):
        """Sets the max_login_tries of this Settings.


        :param max_login_tries: The max_login_tries of this Settings.
        :type max_login_tries: int
        """
        if max_login_tries is not None and max_login_tries > 2147483647:  # noqa: E501
            raise ValueError("Invalid value for `max_login_tries`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if max_login_tries is not None and max_login_tries < 0:  # noqa: E501
            raise ValueError("Invalid value for `max_login_tries`, must be a value greater than or equal to `0`")  # noqa: E501

        self._max_login_tries = max_login_tries

    @property
    def block_time(self) -> int:
        """Gets the block_time of this Settings.


        :return: The block_time of this Settings.
        :rtype: int
        """
        return self._block_time

    @block_time.setter
    def block_time(self, block_time: int):
        """Sets the block_time of this Settings.


        :param block_time: The block_time of this Settings.
        :type block_time: int
        """
        if block_time is not None and block_time > 2147483647:  # noqa: E501
            raise ValueError("Invalid value for `block_time`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if block_time is not None and block_time < 0:  # noqa: E501
            raise ValueError("Invalid value for `block_time`, must be a value greater than or equal to `0`")  # noqa: E501

        self._block_time = block_time
