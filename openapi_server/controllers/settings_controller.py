import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.settings import Settings  # noqa: E501
from openapi_server import util


def settings_list():  # noqa: E501
    """display settings

    list all current settings states # noqa: E501


    :rtype: Union[Settings, Tuple[Settings, int], Tuple[Settings, int, Dict[str, str]]
    """
    return 'do some magic!'


def settings_update(settings):  # noqa: E501
    """update settings

    updates settings # noqa: E501

    :param settings: 
    :type settings: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        settings = Settings.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
