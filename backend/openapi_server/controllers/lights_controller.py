import connexion

from openapi_server.models.groups import Groups  # noqa: E501
from openapi_server.models.groups_response import GroupsResponse  # noqa: E501
from openapi_server.models.lights import Lights  # noqa: E501
from openapi_server.models.lights_response import LightsResponse  # noqa: E501
from openapi_server.models.map import Map  # noqa: E501

from openapi_server.db import get_db, close_db
from openapi_server.security import check_sql_inject_json

from openapi_server.security import check_auth

from flask_jwt_extended import jwt_required

from flask import request

import json

from openapi_server.config import get_logging

logging = get_logging()


def light_add(lights):  # noqa: E501
    """add light device

    adds a new Light device # noqa: E501

    :param lights:
    :type lights: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        lights = Lights.from_dict(connexion.request.get_json())  # noqa: E501
    return "do some magic!"


def light_change(lights):  # noqa: E501
    """change light device

    change a Light device # noqa: E501

    :param lights:
    :type lights: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        lights = Lights.from_dict(connexion.request.get_json())  # noqa: E501
    return "do some magic!"


def lights_devices_delete(id):  # noqa: E501
    """delete a light

    deletes a light # noqa: E501

    :param id: The light that needs to be deleted
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return "do some magic!"


def lights_devices_get(limit=None, page=None):  # noqa: E501
    """list lights

    list all light devices # noqa: E501

    :param limit: items per page
    :type limit: int
    :param page: page number
    :type page: int

    :rtype: Union[List[LightsResponse], Tuple[List[LightsResponse], int], Tuple[List[LightsResponse], int, Dict[str, str]]
    """
    return "do some magic!"


@jwt_required()
def lights_group_delete():  # noqa: E501
    if not check_auth("lights"):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()
    
    id = request.args.get("id")

    cursor.execute("SELECT * FROM groups WHERE id = %s", (id,))
    if cursor.fetchone() is None:
        return "Group does not exist", 404

    cursor.execute("DELETE FROM groups WHERE id = %s", (id,))
    db.commit()
    close_db(db)
    
    logging.info(f"Group {id} deleted")
    return "Group deleted", 200


@jwt_required()
def lights_group_get(limit=None, page=None):  # noqa: E501
    if not check_auth():
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    offset = limit * page

    cursor.execute(
        "SELECT * FROM groups ORDER BY id ASC LIMIT %s OFFSET %s", (limit, offset)
    )
    groups = cursor.fetchall()

    for i in range(len(groups)):
        try:
            groups = json.loads(groups[i][7])
        except TypeError:
            groups = []

        groups[i] = GroupsResponse(id=groups[i][0], name=groups[i][1])

    return groups, 200


@jwt_required()
def lights_group_post(groups):  # noqa: E501
    if not check_auth("lights"):
        return "unauthorized", 401

    db = get_db()
    cursor = db.cursor()

    if connexion.request.is_json:
        groups = Groups.from_dict(connexion.request.get_json())  # noqa: E501

        if check_sql_inject_json(groups):
            return "Invalid value", 400

        cursor.execute("SELECT * FROM groups WHERE name = %s", (groups.name,))
        if cursor.fetchone() is not None:
            return "Group already exists", 400

        cursor.execute("INSERT INTO groups (name) VALUES (%s)", (groups.name,))
        db.commit()
        close_db(db)
        return "Group added", 201
    
    logging.warning("Invalid request in lights_group_post")
    return "invalid request", 400


def lights_map_delete(id):  # noqa: E501
    """delete a mapper

    deletes a mapper # noqa: E501

    :param id: The mapper that needs to be deleted
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return "do some magic!"


def lights_map_get(limit=None, page=None):  # noqa: E501
    """list all mappings

    lists all mappings # noqa: E501

    :param limit: items per page
    :type limit: int
    :param page: page number
    :type page: int

    :rtype: Union[List[Map], Tuple[List[Map], int], Tuple[List[Map], int, Dict[str, str]]
    """
    return "do some magic!"


def lights_map_post(map):  # noqa: E501
    """add a light - product mapping

    map a light to a product # noqa: E501

    :param map:
    :type map: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        map = Map.from_dict(connexion.request.get_json())  # noqa: E501
    return "do some magic!"


def lights_map_put(map):  # noqa: E501
    """change a light - product mapping

    change a mapping # noqa: E501

    :param map:
    :type map: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        map = Map.from_dict(connexion.request.get_json())  # noqa: E501
    return "do some magic!"
