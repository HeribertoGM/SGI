import pytest
from config import create_app

@pytest.fixture(scope='module')
def test_client():
	flask_app = create_app()

	flask_app.testing = True
	with flask_app.test_client() as testing_client:
		with flask_app.app_context():
			yield testing_client


@pytest.fixture(scope='function')
def product_id(test_client):
	payload = {
		"name": "Product T",
		"description": "Description of product T",
		"category": "Category T",
		"price": 5.00,
		"sku": "SKUTTT"
	}
	response = test_client.post('/', json=payload)
	obj = response.json

	yield obj['data']['id']
	
	test_client.delete(f'/{obj["data"]["id"]}')
