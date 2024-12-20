import unittest

from flask import json

from openapi_server.models.security_controller_login200_response import SecurityControllerLogin200Response  # noqa: E501
from openapi_server.models.security_controller_login_request import SecurityControllerLoginRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_security_controller_login(self):
        """Test case for security_controller_login

        User Login
        """
        security_controller_login_request = openapi_server.SecurityControllerLoginRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/user/login',
            method='POST',
            headers=headers,
            data=json.dumps(security_controller_login_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
