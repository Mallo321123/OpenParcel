import connexion
from openapi_server.models.products import Products  # noqa: E501
from openapi_server.models.products_response import ProductsResponse  # noqa: E501

from openapi_server.__init__ import get_db, close_db
from openapi_server.tokenManager import valid_token
from openapi_server.permission_check import check_permission

from flask_jwt_extended import jwt_required, get_jwt
from flask import request

import json

@jwt_required()
def product_add(products=None):  # noqa: E501
    
    jwt_data = get_jwt()
    user = jwt_data.get("user")
    
    if check_permission("products", user) is False:
        return "unauthorized", 401
    
    token = request.headers.get("Authorization").split(" ")[1]
    
    if not valid_token(user, token):
        return "unauthorized", 401
    
    db = get_db()
    cursor = db.cursor()
    
    if connexion.request.is_json:
        products = Products.from_dict(connexion.request.get_json())  # noqa: E501
        
        cursor.execute("SELECT * FROM products WHERE name = %s", (products.name,))
        if cursor.fetchone() is not None:
            return "Product already exists", 400
        
        customer_groups_json = json.dumps(products.customer_groups)
        
        try:
            cursor.execute("""INSERT INTO products 
                       (name, comment, customerGroups, difficulty, buildTime) VALUES (%s, %s, %s, %s, %s)""",
                       (products.name, products.comment, customer_groups_json, products.difficulty, products.build_time))
        
        except Exception as e:
            return str(e), 400
        
        db.commit()
        close_db(db)
        
        return "Product created", 200

@jwt_required()
def products_delete(id):  # noqa: E501
    jwt_data = get_jwt()
    user = jwt_data.get("user")
    
    if check_permission("products", user) is False:
        return "unauthorized", 401
    
    token = request.headers.get("Authorization").split(" ")[1]
    
    if not valid_token(user, token):
        return "unauthorized", 401
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    if cursor.fetchone() is None:
        return "Product not found", 400
    
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    db.commit()
    
    close_db(db)
    return "Product deleted", 200

@jwt_required()
def products_list(limit=None, page=None):  # noqa: E501
    jwt_data = get_jwt()
    user = jwt_data.get("user")
    
    if check_permission("products", user) is False:
        return "unauthorized", 401
    
    token = request.headers.get("Authorization").split(" ")[1]
    
    if not valid_token(user, token):
        return "unauthorized", 401
    
    db = get_db()
    cursor = db.cursor()
    
    offset = limit * page

    cursor.execute("SELECT * FROM products ORDER BY id ASC LIMIT %s OFFSET %s", (limit, offset))
    products = cursor.fetchall()
    
    close_db(db)
    
    for i in range(len(products)):
        try:
            customerGroups = json.loads(products[i][3])
        except TypeError:
            customerGroups = []
            
        products[i] = ProductsResponse(
            id=products[i][0],
            name=products[i][1],
            comment=products[i][2],
            customer_groups=customerGroups,
            difficulty=products[i][4],
            build_time=products[i][5]
        )
    
    return products, 200

@jwt_required()
def update_product(name, products=None):  # noqa: E501
    jwt_data = get_jwt()
    user = jwt_data.get("user")
    
    if check_permission("products", user) is False:
        return "unauthorized", 401
    
    token = request.headers.get("Authorization").split(" ")[1]
    
    if not valid_token(user, token):
        return "unauthorized", 401
    
    db = get_db()
    cursor = db.cursor()
    
    if connexion.request.is_json:
        products = Products.from_dict(connexion.request.get_json())  # noqa: E501
        
        if isinstance(products, Products):
            products = products.to_dict()
        
        # Prepare a dictionary of fields to update
        update_fields = {}

        if products.get("buildTime") is not None:
            update_fields['buildTime'] = products['BuildTime']

        if products.get('comment') is not None:
            update_fields['comment'] = products['comment']

        if products.get('customerGroups') is not None:
            customer_groups_json = json.dumps(products['customerGroups'])
            update_fields['customerGroups'] = customer_groups_json
            
        if products.get('difficulty') is not None:
            update_fields['difficulty'] = products['difficulty']
        
        if products.get('name') is not None:
            cursor.execute("SELECT * FROM products WHERE name = %s", (products['name'],))
            if cursor.fetchone() is not None:
                return "Name already taken", 400
            update_fields['name'] = products['name']
            
        if update_fields is None:
            return "No fields to update", 400
        
        # Construct the SQL update statement dynamically
        set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
        values = list(update_fields.values())
        values.append(name)

        update_query = f"UPDATE products SET {set_clause} WHERE name = %s"

        try:
            cursor.execute(update_query, tuple(values))
            db.commit()
        except Exception as e:
            db.rollback()
            return f"Failed to update product: {e}", 500
        finally:
            close_db(db)
        
        return "Product updated", 200
    return "Invalid input", 400
