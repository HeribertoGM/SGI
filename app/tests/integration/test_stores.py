
def test_stores_health(stores_client):
	"""
	GIVEN a Flask application
	WHEN the '/health' page is requested (GET)
	THEN check that the response is valid
	"""
	response = stores_client.get('/health')
	assert response.status_code == 200
	assert response.json['ok']
	assert response.json['from'] == 'stores'

def test_stores_list(stores_client):
	"""
	GIVEN a Flask application
	WHEN the '/<string:store_id>' page is requested (GET)
	THEN check that the response is valid
	"""
	store_id = "<UUID_FOR_STORE_5>"
	response = stores_client.get(f'/{store_id}/inventory')
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 4
	assert obj['data'][0]['store_id'] == store_id

def test_stores_list_store_not_found(stores_client):
	"""
	GIVEN a Flask application
	WHEN the '/<string:store_id>' page is requested (GET) with a non existent store_id
	THEN check that the response is valid
	"""
	store_id = "<UUID_FOR_STORE_T>"
	response = stores_client.get(f'/{store_id}/inventory')
	obj = response.json
	assert response.status_code == 200
	assert obj['ok']
	assert obj['length'] == 0