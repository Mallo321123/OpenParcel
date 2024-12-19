import unittest

from flask import json

from openapi_server.models.user import User  # noqa: E501
from openapi_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_create_user(self):
        """Test case for create_user

        Create user
        """
        user = {"firstName":"John","lastName":"James","userGroups":["[\"admin\",\"products\",\"users\",\"lights\",\"statistics\"]","[\"admin\",\"products\",\"users\",\"lights\",\"statistics\"]"],"password":"12345","userStatus":1,"email":"john@email.com","username":"theUser"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/user',
            method='POST',
            headers=headers,
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_user(self):
        """Test case for delete_user

        Delete user
        """
        query_string = [('username', 'username_example')]
        headers = { 
        }
        response = self.client.open(
            '/api/user',
            method='DELETE',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user_by_name(self):
        """Test case for get_user_by_name

        Get user by user name
        """
        query_string = [('username', 'username_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/user',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_user(self):
        """Test case for login_user

        Logs user into the system
        """
        query_string = [('username', 'username_example'),
                        ('password', 'password_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/user/login',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout_user(self):
        """Test case for logout_user

        Logs out current logged in user session
        """
        headers = { 
        }
        response = self.client.open(
            '/api/user/logout',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_user(self):
        """Test case for update_user

        Update user
        """
        user = {"firstName":"John","lastName":"James","userGroups":["[\"admin\",\"products\",\"users\",\"lights\",\"statistics\"]","[\"admin\",\"products\",\"users\",\"lights\",\"statistics\"]"],"password":"12345","userStatus":1,"email":"john@email.com","username":"theUser"}
        query_string = [('username', 'username_example')]
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/user',
            method='PUT',
            headers=headers,
            data=json.dumps(user),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_list_get(self):
        """Test case for user_list_get

        list users
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/user/list',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
