from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class TooManyRequests(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, message=None):  # noqa: E501
        """TooManyRequests - a model defined in OpenAPI

        :param message: The message of this TooManyRequests.  # noqa: E501
        :type message: str
        """
        self.openapi_types = {
            'message': str
        }

        self.attribute_map = {
            'message': 'message'
        }

        self._message = message

    @classmethod
    def from_dict(cls, dikt) -> 'TooManyRequests':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TooManyRequests of this TooManyRequests.  # noqa: E501
        :rtype: TooManyRequests
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message(self) -> str:
        """Gets the message of this TooManyRequests.


        :return: The message of this TooManyRequests.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this TooManyRequests.


        :param message: The message of this TooManyRequests.
        :type message: str
        """
        if message is not None and len(message) > 255:
            raise ValueError("Invalid value for `message`, length must be less than or equal to `255`")  # noqa: E501

        self._message = message
