from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class NotFound(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, message=None):  # noqa: E501
        """NotFound - a model defined in OpenAPI

        :param message: The message of this NotFound.  # noqa: E501
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
    def from_dict(cls, dikt) -> 'NotFound':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NotFound of this NotFound.  # noqa: E501
        :rtype: NotFound
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message(self) -> str:
        """Gets the message of this NotFound.


        :return: The message of this NotFound.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this NotFound.


        :param message: The message of this NotFound.
        :type message: str
        """
        if message is not None and len(message) > 255:
            raise ValueError("Invalid value for `message`, length must be less than or equal to `255`")  # noqa: E501

        self._message = message
