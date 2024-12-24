import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.groups import Groups  # noqa: E501
from openapi_server.models.lights import Lights  # noqa: E501
from openapi_server.models.map import Map  # noqa: E501
from openapi_server import util


def light_add(lights):  # noqa: E501
    """add light device

    adds a new Light device # noqa: E501

    :param lights: 
    :type lights: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        lights = Lights.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def light_change(lights):  # noqa: E501
    """change light device

    change a Light device # noqa: E501

    :param lights: 
    :type lights: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        lights = Lights.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def lights_devices_delete(id):  # noqa: E501
    """delete a light

    deletes a light # noqa: E501

    :param id: The light that needs to be deleted
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def lights_devices_get(limit=None, page=None):  # noqa: E501
    """list lights

    list all light devices # noqa: E501

    :param limit: items per page
    :type limit: int
    :param page: page number
    :type page: int

    :rtype: Union[List[Lights], Tuple[List[Lights], int], Tuple[List[Lights], int, Dict[str, str]]
    """
    return 'do some magic!'


def lights_group_delete(id):  # noqa: E501
    """delete a light group

    deletes a light grouo # noqa: E501

    :param id: The group that needs to be deleted
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def lights_group_get(limit=None, page=None):  # noqa: E501
    """list all light groups

    returns all light groups # noqa: E501

    :param limit: items per page
    :type limit: int
    :param page: page number
    :type page: int

    :rtype: Union[List[Groups], Tuple[List[Groups], int], Tuple[List[Groups], int, Dict[str, str]]
    """
    return 'do some magic!'


def lights_group_post(groups):  # noqa: E501
    """add light group

    adds a new Light group # noqa: E501

    :param groups: 
    :type groups: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        groups = Groups.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def lights_map_delete(id):  # noqa: E501
    """delete a mapper

    deletes a mapper # noqa: E501

    :param id: The mapper that needs to be deleted
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def lights_map_get(limit=None, page=None):  # noqa: E501
    """list all mappings

    lists all mappings # noqa: E501

    :param limit: items per page
    :type limit: int
    :param page: page number
    :type page: int

    :rtype: Union[List[Map], Tuple[List[Map], int], Tuple[List[Map], int, Dict[str, str]]
    """
    return 'do some magic!'


def lights_map_post(map):  # noqa: E501
    """add a light - product mapping

    map a light to a product # noqa: E501

    :param map: 
    :type map: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        map = Map.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def lights_map_put(map):  # noqa: E501
    """change a light - product mapping

    change a mapping # noqa: E501

    :param map: 
    :type map: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        map = Map.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
