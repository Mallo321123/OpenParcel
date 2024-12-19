import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.dashboard import Dashboard  # noqa: E501
from openapi_server import util


def dashboard_get():  # noqa: E501
    """list dashboard information

    lists dashboard information # noqa: E501


    :rtype: Union[List[Dashboard], Tuple[List[Dashboard], int], Tuple[List[Dashboard], int, Dict[str, str]]
    """
    return 'do some magic!'
