import pytest

def test_products_health(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/health' page is requested (GET)
	THEN check that the response is valid
	"""
	response = test_client.get('/health')
	assert response.status_code == 200
	assert response.json['ok']

def test_products_list(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET)
	THEN check that the response is valid
	"""
	response = test_client.get('/')
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert 'name' in obj['data'][0].keys()
	assert 'description' in obj['data'][0].keys()
	assert 'category' in obj['data'][0].keys()
	assert 'price' in obj['data'][0].keys()
	assert 'sku' in obj['data'][0].keys()
	assert obj['data'][0]['stock'] >= 0

def test_products_list_filter_category(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with 'category' filter param
	THEN check that the response is valid
	"""
	params = {
		'category': 'Category A'
	}
	response = test_client.get('/', query_string=params)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 8
	assert obj['total'] == 8
	assert obj['data'][0]['category'] == params['category']

def test_products_list_filter_sku(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with 'sku' filter param
	THEN check that the response is valid
	"""
	params = {
		'sku': 'SKU003'
	}
	response = test_client.get('/', query_string=params)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 1
	assert obj['total'] == 1
	assert obj['data'][0]['sku'] == params['sku']

def test_products_list_filter_min_price(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with 'min_price' filter param
	THEN check that the response is valid
	"""
	params = {
		'minPrice': 10
	}
	response = test_client.get('/', query_string=params)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 10
	assert obj['total'] == 16
	assert float(obj['data'][0]['price']) >= params['minPrice']

def test_products_list_filter_max_price(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with 'max_price' filter param
	THEN check that the response is valid
	"""
	params = {
		'maxPrice': 20
	}
	response = test_client.get('/', query_string=params)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 10
	assert obj['total'] == 13
	assert float(obj['data'][0]['price']) <= params['maxPrice']

def test_products_list_filter_min_stock(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with 'min_stock' filter param
	THEN check that the response is valid
	"""
	params = {
		'minStock': 100
	}
	response = test_client.get('/', query_string=params)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 10
	assert obj['total'] == 11
	assert int(obj['data'][0]['stock']) >= params['minStock']

def test_products_list_filter_max_stock(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with 'max_stock' filter param
	THEN check that the response is valid
	"""
	params = {
		'maxStock': 200
	}
	response = test_client.get('/', query_string=params)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 10
	assert obj['total'] == 17
	assert int(obj['data'][0]['stock']) <= params['maxStock']

def test_products_list_pagination(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with 'page' param
	THEN check that the response is valid
	"""
	response1 = test_client.get('/')
	params = {
		'page': 1
	}
	response2 = test_client.get('/', query_string=params)
	obj1 = response1.json
	obj2 = response2.json
	assert response1.status_code == 200
	assert response2.status_code == 200
	assert obj1['ok']
	assert obj2['ok']
	assert obj1['data'][0]['sku'] != obj2['data'][0]['sku']

def test_products_list_pagination_size(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with 'perPage' param
	THEN check that the response is valid
	"""
	params = {
		'perPage': 15
	}
	response = test_client.get('/', query_string=params)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 15

def test_products_list_order(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with 'order' param
	THEN check that the response is valid
	"""
	params = {
		'orderBy': 'stock'
	}
	response = test_client.get('/', query_string=params)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert int(obj['data'][1]['stock']) <= int(obj['data'][2]['stock'])

def test_products_list_multiple(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with 'min_stock', 'max_stock' 'pagination' and 'order' params
	THEN check that the response is valid
	"""
	params = {
		'minStock': 100,
		'maxStock': 200,
		'perPage': 5,
		'orderBy': 'stock'
	}
	response = test_client.get('/', query_string=params)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 5
	assert obj['total'] == 7
	assert int(obj['data'][1]['stock']) <= int(obj['data'][2]['stock'])

def test_products_list_order_wrong_field(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with a non existent column in 'order' param
	THEN check that the response is valid
	"""
	params = {
		'orderBy': 'column'
	}
	response = test_client.get('/', query_string=params)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['data'][0]['sku'] < obj['data'][1]['sku']

def test_products_list_wrong_type(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET) with a wrong data type value as param
	THEN check that the response is valid
	"""
	params = {
		'category': 20
	}
	response = test_client.get('/', query_string=params)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 0
	assert obj['total'] == 0

def test_products_new(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (POST) with new item data as payload
	THEN check that the response is valid
	"""
	payload = {
		"name": "Product T",
		"description": "Description of product T",
		"category": "Category T",
		"price": 5.00,
		"sku": "SKUTTT"
	}
	response = test_client.post('/', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['data']['id'] != None
	assert obj['payload'] == payload
	test_client.delete(f'/{obj["data"]["id"]}')

def test_products_new_ltz_price(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (POST) with new item data as payload and price is lower than zero
	THEN check that the response is valid
	"""
	payload = {
		"name": "Product T",
		"description": "Description of product T",
		"category": "Category T",
		"price": -1.00,
		"sku": "SKUTTT"
	}
	response = test_client.post('/', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "FieldConstraintViolation"
	assert obj['payload'] == payload

def test_products_new_missing_field(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (POST) with new item data as payload and there is a missing field
	THEN check that the response is valid
	"""
	payload = {
		"name": "Product T",
		"description": "Description of product T",
		"category": "Category T",
		"sku": "SKUTTT"
	}
	response = test_client.post('/', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "MissingKey"
	assert obj['payload'] == payload

def test_products_new_wrong_type(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (POST) with new item data as payload and there is a wrong data type
	THEN check that the response is valid
	"""
	payload = {
		"name": "Product T",
		"description": "Description of product T",
		"category": "Category T",
		"price": 5.00,
		"sku": 86
	}
	response = test_client.post('/', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "WrongDataType"
	assert obj['payload'] == payload

def test_products_detail(test_client, product_id):
	"""
	GIVEN a Flask application
	WHEN the '/<uuid:product_id>' page is requested (GET)
	THEN check that the response is valid
	"""
	response = test_client.get(f'/{product_id}')
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['data']['id'] == product_id

def test_products_detail_not_found(test_client, product_id):
	"""
	GIVEN a Flask application
	WHEN the '/<uuid:product_id>' page is requested (GET) with a non existent uuid
	THEN check that the response is valid
	"""
	new_id = "86" + product_id[2:]
	response = test_client.get(f'/{new_id}')
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "NoResultFound"

def test_products_detail_not_uuid(test_client, product_id):
	"""
	GIVEN a Flask application
	WHEN the '/<uuid:product_id>' page is requested (GET) with a non uuid id
	THEN check that the response is valid
	"""
	response = test_client.get(f'/{product_id[2:]}')
	obj = response.json
	assert response.status_code == 404
	assert obj['ok'] == False
	assert obj['error'] == "404 - Not Found"

def test_products_update(test_client, product_id):
	"""
	GIVEN a Flask application
	WHEN the '/<uuid:product_id>' page is requested (PUT)
	THEN check that the response is valid
	"""
	payload = {
		"category": "Category T2",
	}
	response = test_client.put(f'/{product_id}', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['data']['id'] == product_id
	assert obj['data']['category'] == payload['category']

def test_products_update_ltz_price(test_client, product_id):
	"""
	GIVEN a Flask application
	WHEN the '/<uuid:product_id>' page is requested (PUT) with a price lower than zero
	THEN check that the response is valid
	"""
	payload = {
		"price": -1.00,
	}
	response = test_client.put(f'/{product_id}', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == 'FieldConstraintViolation'

def test_products_update_wrong_type(test_client, product_id):
	"""
	GIVEN a Flask application
	WHEN the '/<uuid:product_id>' page is requested (PUT) with a wrong category data type
	THEN check that the response is valid
	"""
	payload = {
		"category": 86,
	}
	response = test_client.put(f'/{product_id}', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == 'WrongDataType'

def test_products_update_not_found(test_client, product_id):
	"""
	GIVEN a Flask application
	WHEN the '/<uuid:product_id>' page is requested (PUT) with a non existent uuid
	THEN check that the response is valid
	"""
	new_id = "86" + product_id[2:]
	payload = {
		"category": "Category T2",
	}
	response = test_client.put(f'/{new_id}', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "NoResultFound"

def test_products_update_not_uuid(test_client, product_id):
	"""
	GIVEN a Flask application
	WHEN the '/<uuid:product_id>' page is requested (PUT) with a non uuid id
	THEN check that the response is valid
	"""
	payload = {
		"category": "Category T2",
	}
	response = test_client.put(f'/{product_id[2:]}', json=payload)
	obj = response.json
	assert response.status_code == 404
	assert obj['ok'] == False
	assert obj['error'] == "404 - Not Found"

def test_products_delete(test_client, product_id):
	"""
	GIVEN a Flask application
	WHEN the '/<uuid:product_id>' page is requested (DELETE)
	THEN check that the response is valid
	"""
	response = test_client.delete(f'/{product_id}')
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['data']['id'] == product_id
	assert obj['payload']['product_id'] == product_id

def test_products_delete_not_found(test_client, product_id):
	"""
	GIVEN a Flask application
	WHEN the '/<uuid:product_id>' page is requested (DELETE) with a non existent uuid
	THEN check that the response is valid
	"""
	new_id = "86" + product_id[2:]
	response = test_client.delete(f'/{new_id}')
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "NoResultFound"

def test_products_delete_not_uuid(test_client, product_id):
	"""
	GIVEN a Flask application
	WHEN the '/<uuid:product_id>' page is requested (DELETE) with a non uuid id
	THEN check that the response is valid
	"""
	response = test_client.delete(f'/{product_id[2:]}')
	obj = response.json
	assert response.status_code == 404
	assert obj['ok'] == False
	assert obj['error'] == "404 - Not Found"