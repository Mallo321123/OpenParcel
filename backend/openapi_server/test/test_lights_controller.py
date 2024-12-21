import unittest

from flask import json

from openapi_server.models.groups import Groups  # noqa: E501
from openapi_server.models.lights import Lights  # noqa: E501
from openapi_server.models.map import Map  # noqa: E501
from openapi_server.test import BaseTestCase


class TestLightsController(BaseTestCase):
    """LightsController integration test stubs"""

    def test_light_add(self):
        """Test case for light_add

        add light device
        """
        lights = {"note":"example note","groups":{"name":"regal rechts","id":1},"online":1,"adress":"wled1.local","id":1}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/lights/devices',
            method='POST',
            headers=headers,
            data=json.dumps(lights),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_light_change(self):
        """Test case for light_change

        change light device
        """
        lights = {"note":"example note","groups":{"name":"regal rechts","id":1},"online":1,"adress":"wled1.local","id":1}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/lights/devices',
            method='PUT',
            headers=headers,
            data=json.dumps(lights),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lights_devices_delete(self):
        """Test case for lights_devices_delete

        delete a light
        """
        query_string = [('id', 56)]
        headers = { 
        }
        response = self.client.open(
            '/api/lights/devices',
            method='DELETE',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lights_devices_get(self):
        """Test case for lights_devices_get

        list lights
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/lights/devices',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lights_group_delete(self):
        """Test case for lights_group_delete

        delete a light group
        """
        query_string = [('id', 56)]
        headers = { 
        }
        response = self.client.open(
            '/api/lights/group',
            method='DELETE',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lights_group_get(self):
        """Test case for lights_group_get

        list all light groups
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/lights/group',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lights_group_post(self):
        """Test case for lights_group_post

        add light group
        """
        groups = {"name":"regal rechts","id":1}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/lights/group',
            method='POST',
            headers=headers,
            data=json.dumps(groups),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lights_map_delete(self):
        """Test case for lights_map_delete

        delete a mapper
        """
        query_string = [('id', 56)]
        headers = { 
        }
        response = self.client.open(
            '/api/lights/map',
            method='DELETE',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lights_map_get(self):
        """Test case for lights_map_get

        list all mappings
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/lights/map',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lights_map_post(self):
        """Test case for lights_map_post

        add a light - product mapping
        """
        map = {"productId":[10,10],"name":"blinky","id":1,"lightId":[5,5]}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/lights/map',
            method='POST',
            headers=headers,
            data=json.dumps(map),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lights_map_put(self):
        """Test case for lights_map_put

        change a light - product mapping
        """
        map = {"productId":[10,10],"name":"blinky","id":1,"lightId":[5,5]}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/lights/map',
            method='PUT',
            headers=headers,
            data=json.dumps(map),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
