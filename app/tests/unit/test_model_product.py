
def test_create_correct_product():
	"""
	GIVEN a Product model
	WHEN a new Product is created
	THEN check the name, description, category, price and sku are defined correctly
	"""
	obj = {
		"name": "Testing Product",
		"description": "This is a testing product",
		"category": "Category T",
		"price": 999.99,
		"sku": "SKUTTT"
	}
	from models.product import Product
	product = Product(obj)
	assert vars(product)['name'] == obj['name']
	assert vars(product)['description'] == obj['description']
	assert vars(product)['category'] == obj['category']
	assert vars(product)['price'] == obj['price']
	assert vars(product)['sku'] == obj['sku']

def test_create_ltz_price_product():
	"""
	GIVEN a Product model
	WHEN a new Product is created with a price field value less than zero
	THEN check the exception raised == FieldConstraintViolation
	"""
	obj = {
		"name": "Testing Product",
		"description": "This is a testing product",
		"category": "Category T",
		"price": -1.00,
		"sku": "SKUTTT"
	}
	try:
		from models.product import Product
		product = Product(obj)
	except Exception as ex:
		assert ex.args[0] == "FieldConstraintViolation"

def test_create_missing_field_product():
	"""
	GIVEN a Product model
	WHEN a new Product is created with a missing field
	THEN check the exception raised == MissingKey
	"""
	obj = {
		"description": "This is a testing product",
		"category": "Category T",
		"price": 999.99,
		"sku": "SKUTTT"
	}
	try:
		from models.product import Product
		product = Product(obj)
	except Exception as ex:
		assert ex.args[0] == "MissingKey"

def test_create_wrong_type_product():
	"""
	GIVEN a Product model
	WHEN a new Product is created with a wrong type field
	THEN check the exception raised == WrongDataType
	"""
	obj = {
		"name": "Testing Product",
		"description": "This is a testing product",
		"category": 86,
		"price": 999.99,
		"sku": "SKUTTT"
	}
	try:
		from models.product import Product
		product = Product(obj)
	except Exception as ex:
		assert ex.args[0] == "WrongDataType"

def test_update_correct_product():
	"""
	GIVEN a Product model
	WHEN a Product is updated
	THEN check the category and price fields were updated correctly
	"""
	obj = {
		"name": "Testing Product",
		"description": "This is a testing product",
		"category": "Category T",
		"price": 999.99,
		"sku": "SKUTTT"
	}
	from models.product import Product
	product = Product(obj)
	
	product.update({'category': 'Category T2', 'price': 10.00})
	assert vars(product)['category'] == 'Category T2'
	assert vars(product)['price'] == 10.00
	
def test_update_ltz_price_product():
	"""
	GIVEN a Product model
	WHEN a Product is updated with a price field value less than zero
	THEN check the exception raised == FieldConstraintViolation
	"""
	obj = {
		"name": "Testing Product",
		"description": "This is a testing product",
		"category": "Category T",
		"price": 999.99,
		"sku": "SKUTTT"
	}
	from models.product import Product
	product = Product(obj)
	try:
		product.update({'category': 'Category T2', 'price': -1.00})
	except Exception as ex:
		assert ex.args[0] == "FieldConstraintViolation"

def test_update_wrong_type_product():
	"""
	GIVEN a Product model
	WHEN a Product is updated with a wrong type field
	THEN check the exception raised == WrongDataType
	"""
	obj = {
		"name": "Testing Product",
		"description": "This is a testing product",
		"category": "Category T",
		"price": 999.99,
		"sku": "SKUTTT"
	}
	from models.product import Product
	product = Product(obj)
	try:
		product.update({'category': 86, 'price': 10.00})
	except Exception as ex:
		assert ex.args[0] == "WrongDataType"