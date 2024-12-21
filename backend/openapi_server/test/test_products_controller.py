import unittest

from flask import json

from openapi_server.models.products import Products  # noqa: E501
from openapi_server.test import BaseTestCase


class TestProductsController(BaseTestCase):
    """ProductsController integration test stubs"""

    def test_product_add(self):
        """Test case for product_add

        add a product
        """
        products = {"difficulty":3,"customerGroups":["[\"adults\",\"teens\",\"kids\",\"nerds\"]","[\"adults\",\"teens\",\"kids\",\"nerds\"]"],"buildTime":"20-30 min","name":"openDTU","comment":"example comment","id":1}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/products',
            method='POST',
            headers=headers,
            data=json.dumps(products),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_delete(self):
        """Test case for products_delete

        delete a product
        """
        query_string = [('id', 56)]
        headers = { 
        }
        response = self.client.open(
            '/api/products',
            method='DELETE',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_list(self):
        """Test case for products_list

        list of products
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/products',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_product(self):
        """Test case for update_product

        update product
        """
        products = {"difficulty":3,"customerGroups":["[\"adults\",\"teens\",\"kids\",\"nerds\"]","[\"adults\",\"teens\",\"kids\",\"nerds\"]"],"buildTime":"20-30 min","name":"openDTU","comment":"example comment","id":1}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/products',
            method='PUT',
            headers=headers,
            data=json.dumps(products),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
