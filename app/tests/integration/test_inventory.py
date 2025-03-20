
def test_inventory_health(inventory_client):
	"""
	GIVEN a Flask application
	WHEN the '/health' page is requested (GET)
	THEN check that the response is valid
	"""
	response = inventory_client.get('/health')
	assert response.status_code == 200
	assert response.json['ok']
	assert response.json['from'] == 'inventory'

def test_inventory_alerts(inventory_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET)
	THEN check that the response is valid
	"""
	response = inventory_client.get(f'/alerts')
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 1
	assert obj['data'][0]['quantity'] < obj['data'][0]['min_stock']

def test_inventory_transfer_transfer(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "TRANSFER" type item data as payload
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"source_store_id": "<UUID_FOR_STORE_2>",
		"target_store_id": "<UUID_FOR_STORE_4>",
		"quantity": 10,
		"type": "TRANSFER"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['data']['source']['store_id'] == payload['source_store_id']
	assert obj['data']['target']['store_id'] == payload['target_store_id']
	assert obj['data']['source']['quantity'] == 130
	assert obj['data']['target']['quantity'] == 140

def test_inventory_in_transfer(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "IN" type item data as payload
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"target_store_id": "<UUID_FOR_STORE_4>",
		"quantity": 10,
		"type": "IN"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['data']['target']['store_id'] == payload['target_store_id']
	assert obj['data']['target']['quantity'] == 140

def test_inventory_out_transfer(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "OUT" type item data as payload
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"source_store_id": "<UUID_FOR_STORE_2>",
		"quantity": 10,
		"type": "OUT"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['data']['source']['store_id'] == payload['source_store_id']
	assert obj['data']['source']['quantity'] == 130

def test_inventory_transfer_transfer_missing_field(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "TRANSFER" type item data as payload with a field missing
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"source_store_id": "<UUID_FOR_STORE_2>",
		"target_store_id": "<UUID_FOR_STORE_4>",
		"type": "TRANSFER"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "MissingKey"

def test_inventory_in_transfer_missing_field(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "IN" type item data as payload with a field missing
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"source_store_id": "<UUID_FOR_STORE_2>",
		"quantity": 10,
		"type": "IN"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "MissingKey"

def test_inventory_out_transfer_missing_field(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "OUT" type item data as payload with a field missing
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"target_store_id": "<UUID_FOR_STORE_4>",
		"quantity": 10,
		"type": "OUT"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "MissingKey"

def test_inventory_transfer_ltz_quantity(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "TRANSFER" type item data as payload with quantity field less than zero
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"source_store_id": "<UUID_FOR_STORE_2>",
		"target_store_id": "<UUID_FOR_STORE_4>",
		"quantity": -1,
		"type": "TRANSFER"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "FieldConstraintViolation"

def test_inventory_transfer_wrong_enum_type(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "TRANSFER" type item data as payload with a undefined operation type
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"source_store_id": "<UUID_FOR_STORE_2>",
		"target_store_id": "<UUID_FOR_STORE_4>",
		"quantity": 10,
		"type": "NOOP"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "FieldConstraintViolation"

def test_inventory_transfer_same_source_target(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "TRANSFER" type item data with the same source and target
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"source_store_id": "<UUID_FOR_STORE_2>",
		"target_store_id": "<UUID_FOR_STORE_2>",
		"quantity": 10,
		"type": "TRANSFER"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "FieldConstraintViolation"

def test_inventory_transfer_not_enough_stock(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "TRANSFER" type item data with quantity higher than source stock
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"source_store_id": "<UUID_FOR_STORE_2>",
		"target_store_id": "<UUID_FOR_STORE_4>",
		"quantity": 10000,
		"type": "TRANSFER"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "FieldConstraintViolation"

def test_inventory_transfer_source_inventory_not_found(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "TRANSFER" type item data with no inventary entry on source
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"source_store_id": "<UUID_FOR_STORE_H>",
		"target_store_id": "<UUID_FOR_STORE_4>",
		"quantity": 10,
		"type": "TRANSFER"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok'] == False
	assert obj['error'] == "NoResultFound"

def test_inventory_transfer_target_inventory_not_found(inventory_client, product_id_n_reset):
	"""
	GIVEN a Flask application
	WHEN the '/transfer' page is requested (POST) with new "TRANSFER" type item data with no inventary entry on target
	THEN check that the response is valid
	"""
	payload = {
		"product_id": product_id_n_reset,
		"source_store_id": "<UUID_FOR_STORE_2>",
		"target_store_id": "<UUID_FOR_STORE_T>",
		"quantity": 10,
		"type": "TRANSFER"
	}
	response = inventory_client.post('/transfer', json=payload)
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['data']['source']['store_id'] == payload['source_store_id']
	assert obj['data']['target']['store_id'] == payload['target_store_id']
	assert obj['data']['source']['quantity'] == 130
	assert obj['data']['target']['quantity'] == 10