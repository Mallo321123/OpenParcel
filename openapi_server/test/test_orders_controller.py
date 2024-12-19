import unittest

from flask import json

from openapi_server.models.orders import Orders  # noqa: E501
from openapi_server.test import BaseTestCase


class TestOrdersController(BaseTestCase):
    """OrdersController integration test stubs"""

    def test_orders_delete(self):
        """Test case for orders_delete

        delete a order
        """
        query_string = [('id', 56)]
        headers = { 
        }
        response = self.client.open(
            '/api/orders',
            method='DELETE',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_orders_get(self):
        """Test case for orders_get

        list all orders
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/orders',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_orders_post(self):
        """Test case for orders_post

        add an order
        """
        orders = {"dateAdd":"2024-12-19T20:35:19.772Z","id":5610,"state":"open","dateClosed":"2024-12-19T20:35:19.772Z","customer":"Max Mustermann","products":[{"difficulty":3,"customerGroups":["[\"adults\",\"teens\",\"kids\",\"nerds\"]","[\"adults\",\"teens\",\"kids\",\"nerds\"]"],"buildTime":"20-30 min","name":"openDTU","comment":"example comment","id":1},{"difficulty":3,"customerGroups":["[\"adults\",\"teens\",\"kids\",\"nerds\"]","[\"adults\",\"teens\",\"kids\",\"nerds\"]"],"buildTime":"20-30 min","name":"openDTU","comment":"example comment","id":1}]}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/orders',
            method='POST',
            headers=headers,
            data=json.dumps(orders),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_orders_put(self):
        """Test case for orders_put

        update an order
        """
        orders = {"dateAdd":"2024-12-19T20:35:19.772Z","id":5610,"state":"open","dateClosed":"2024-12-19T20:35:19.772Z","customer":"Max Mustermann","products":[{"difficulty":3,"customerGroups":["[\"adults\",\"teens\",\"kids\",\"nerds\"]","[\"adults\",\"teens\",\"kids\",\"nerds\"]"],"buildTime":"20-30 min","name":"openDTU","comment":"example comment","id":1},{"difficulty":3,"customerGroups":["[\"adults\",\"teens\",\"kids\",\"nerds\"]","[\"adults\",\"teens\",\"kids\",\"nerds\"]"],"buildTime":"20-30 min","name":"openDTU","comment":"example comment","id":1}]}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/orders',
            method='PUT',
            headers=headers,
            data=json.dumps(orders),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
