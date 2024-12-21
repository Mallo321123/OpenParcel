import unittest

from flask import json

from openapi_server.models.dashboard import Dashboard  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDashboardController(BaseTestCase):
    """DashboardController integration test stubs"""

    def test_dashboard_get(self):
        """Test case for dashboard_get

        list dashboard information
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/dashboard',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
