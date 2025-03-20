import pytest
import os
from config import create_app

@pytest.fixture(scope='module')
def inventory_client():
	os.environ['MODULES'] = "[inventory]"

	flask_app = create_app()

	flask_app.testing = True
	with flask_app.test_client() as testing_client:
		with flask_app.app_context():
			yield testing_client

@pytest.fixture(scope='function')
def product_id_n_reset():
	from config import db
	from models.product import Product
	from models.inventory import Inventory

	product = Product.query.filter_by(sku='SKU018').one()
	product_id = getattr(product, 'id')

	yield product_id

	inv1 = Inventory.query.filter_by(product_id=product_id, store_id='<UUID_FOR_STORE_2>').one()
	inv2 = Inventory.query.filter_by(product_id=product_id, store_id='<UUID_FOR_STORE_4>').one()
	inv_t = Inventory.query.filter_by(store_id='<UUID_FOR_STORE_T>').one_or_none()

	inv1.update({'quantity':140})
	inv2.update({'quantity':130})
	if inv_t != None:
		db.session.delete(inv_t)

	db.session.commit()

@pytest.fixture(scope='module')
def stores_client():
	os.environ['MODULES'] = "[stores]"

	flask_app = create_app()

	flask_app.testing = True
	with flask_app.test_client() as testing_client:
		with flask_app.app_context():
			yield testing_client

@pytest.fixture(scope='module')
def products_client():
	os.environ['MODULES'] = "[products]"

	flask_app = create_app()

	flask_app.testing = True
	with flask_app.test_client() as testing_client:
		with flask_app.app_context():
			yield testing_client


@pytest.fixture(scope='function')
def product_id(products_client):
	payload = {
		"name": "Product T",
		"description": "Description of product T",
		"category": "Category T",
		"price": 5.00,
		"sku": "SKUTTT"
	}
	response = products_client.post('/', json=payload)
	obj = response.json

	yield obj['data']['id']
	
	products_client.delete(f'/{obj["data"]["id"]}')
