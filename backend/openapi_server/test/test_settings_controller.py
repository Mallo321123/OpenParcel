import unittest

from flask import json

from openapi_server.models.settings import Settings  # noqa: E501
from openapi_server.test import BaseTestCase


class TestSettingsController(BaseTestCase):
    """SettingsController integration test stubs"""

    def test_settings_list(self):
        """Test case for settings_list

        display settings
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/settings',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_settings_update(self):
        """Test case for settings_update

        update settings
        """
        settings = {"minPasswordLength":5}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/settings',
            method='PUT',
            headers=headers,
            data=json.dumps(settings),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
