from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
import re
from openapi_server import util

import re  # noqa: E501

class LightsResponse(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, groups=None, adress=None, comment=None, online=None):  # noqa: E501
        """LightsResponse - a model defined in OpenAPI

        :param id: The id of this LightsResponse.  # noqa: E501
        :type id: int
        :param groups: The groups of this LightsResponse.  # noqa: E501
        :type groups: List[str]
        :param adress: The adress of this LightsResponse.  # noqa: E501
        :type adress: str
        :param comment: The comment of this LightsResponse.  # noqa: E501
        :type comment: str
        :param online: The online of this LightsResponse.  # noqa: E501
        :type online: int
        """
        self.openapi_types = {
            'id': int,
            'groups': List[str],
            'adress': str,
            'comment': str,
            'online': int
        }

        self.attribute_map = {
            'id': 'id',
            'groups': 'groups',
            'adress': 'adress',
            'comment': 'comment',
            'online': 'online'
        }

        self._id = id
        self._groups = groups
        self._adress = adress
        self._comment = comment
        self._online = online

    @classmethod
    def from_dict(cls, dikt) -> 'LightsResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Lights_response of this LightsResponse.  # noqa: E501
        :rtype: LightsResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this LightsResponse.


        :return: The id of this LightsResponse.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this LightsResponse.


        :param id: The id of this LightsResponse.
        :type id: int
        """
        if id is not None and id > 2147483647:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if id is not None and id < 0:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value greater than or equal to `0`")  # noqa: E501

        self._id = id

    @property
    def groups(self) -> List[str]:
        """Gets the groups of this LightsResponse.


        :return: The groups of this LightsResponse.
        :rtype: List[str]
        """
        return self._groups

    @groups.setter
    def groups(self, groups: List[str]):
        """Sets the groups of this LightsResponse.


        :param groups: The groups of this LightsResponse.
        :type groups: List[str]
        """
        if groups is not None and len(groups) > 100:
            raise ValueError("Invalid value for `groups`, number of items must be less than or equal to `100`")  # noqa: E501

        self._groups = groups

    @property
    def adress(self) -> str:
        """Gets the adress of this LightsResponse.


        :return: The adress of this LightsResponse.
        :rtype: str
        """
        return self._adress

    @adress.setter
    def adress(self, adress: str):
        """Sets the adress of this LightsResponse.


        :param adress: The adress of this LightsResponse.
        :type adress: str
        """
        if adress is not None and len(adress) > 255:
            raise ValueError("Invalid value for `adress`, length must be less than or equal to `255`")  # noqa: E501
        if adress is not None and not re.search(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$|^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$', adress):  # noqa: E501
            raise ValueError(r"Invalid value for `adress`, must be a follow pattern or equal to `/^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$|^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$/`")  # noqa: E501

        self._adress = adress

    @property
    def comment(self) -> str:
        """Gets the comment of this LightsResponse.


        :return: The comment of this LightsResponse.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment: str):
        """Sets the comment of this LightsResponse.


        :param comment: The comment of this LightsResponse.
        :type comment: str
        """
        if comment is not None and len(comment) > 65535:
            raise ValueError("Invalid value for `comment`, length must be less than or equal to `65535`")  # noqa: E501
        if comment is not None and not re.search(r'^[0-9a-z]+$', comment):  # noqa: E501
            raise ValueError(r"Invalid value for `comment`, must be a follow pattern or equal to `/^[0-9a-z]+$/`")  # noqa: E501

        self._comment = comment

    @property
    def online(self) -> int:
        """Gets the online of this LightsResponse.


        :return: The online of this LightsResponse.
        :rtype: int
        """
        return self._online

    @online.setter
    def online(self, online: int):
        """Sets the online of this LightsResponse.


        :param online: The online of this LightsResponse.
        :type online: int
        """
        allowed_values = [1, 0]  # noqa: E501
        if online not in allowed_values:
            raise ValueError(
                "Invalid value for `online` ({0}), must be one of {1}"
                .format(online, allowed_values)
            )

        self._online = online
