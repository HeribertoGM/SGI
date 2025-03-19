
def test_create_correct_inventory():
	"""
	GIVEN a Inventory model
	WHEN a new Inventory is created
	THEN check the product_id, store_id, quantity and min_stock are defined correctly
	"""
	obj = {
		'product_id': "fb9c7029-a328-4c26-8f80-854bf95135c6",
		'store_id': "<UUID_FOR_STORE_T>",
		'quantity': 20,
		'min_stock': 10
	}
	from models.inventory import Inventory
	inventory = Inventory(obj)
	assert vars(inventory)['product_id'] == obj['product_id']
	assert vars(inventory)['store_id'] == obj['store_id']
	assert vars(inventory)['quantity'] == obj['quantity']
	assert vars(inventory)['min_stock'] == obj['min_stock']

def test_create_ltz_quantity_inventory():
	"""
	GIVEN a Inventory model
	WHEN a new Inventory is created with a quantity field value less than zero
	THEN check the exception raised == FieldConstraintViolation
	"""
	obj = {
		'product_id': "fb9c7029-a328-4c26-8f80-854bf95135c6",
		'store_id': "<UUID_FOR_STORE_T>",
		'quantity': -1,
		'min_stock': 10
	}
	try:
		from models.inventory import Inventory
		inventory = Inventory(obj)
	except Exception as ex:
		assert ex.args[0] == "FieldConstraintViolation"
	
def test_create_ltz_min_stock_inventory():
	"""
	GIVEN a Inventory model
	WHEN a new Inventory is created with a min_stock field value less than zero
	THEN check the exception raised == FieldConstraintViolation
	"""
	obj = {
		'product_id': "fb9c7029-a328-4c26-8f80-854bf95135c6",
		'store_id': "<UUID_FOR_STORE_T>",
		'quantity': 20,
		'min_stock': -1
	}
	try:
		from models.inventory import Inventory
		inventory = Inventory(obj)
	except Exception as ex:
		assert ex.args[0] == "FieldConstraintViolation"

def test_create_missing_field_inventory():
	"""
	GIVEN a Inventory model
	WHEN a new Inventory is created with a missing field
	THEN check the exception raised == MissingKey
	"""
	obj = {
		'product_id': "fb9c7029-a328-4c26-8f80-854bf95135c6",
		'quantity': 20,
		'min_stock': 10
	}
	try:
		from models.inventory import Inventory
		inventory = Inventory(obj)
	except Exception as ex:
		assert ex.args[0] == "MissingKey"

def test_create_wrong_type_inventory():
	"""
	GIVEN a Inventory model
	WHEN a new Inventory is created with a wrong type field
	THEN check the exception raised == WrongDataType
	"""
	obj = {
		'product_id': "fb9c7029-a328-4c26-8f80-854bf95135c6",
		'store_id': "<UUID_FOR_STORE_T>",
		'quantity': 20,
		'min_stock': 10.0
	}
	try:
		from models.inventory import Inventory
		inventory = Inventory(obj)
	except Exception as ex:
		assert ex.args[0] == "WrongDataType"

def test_update_correct_inventory():
	"""
	GIVEN a Inventory model
	WHEN a Inventory is updated
	THEN check the store_id and quantity fields were updated correctly
	"""
	obj = {
		'product_id': "fb9c7029-a328-4c26-8f80-854bf95135c6",
		'store_id': "<UUID_FOR_STORE_T>",
		'quantity': 20,
		'min_stock': 10
	}
	from models.inventory import Inventory
	inventory = Inventory(obj)
	
	inventory.update({'store_id': "<UUID_FOR_STORE_T2>", 'quantity': 10})
	assert vars(inventory)['store_id'] == "<UUID_FOR_STORE_T2>"
	assert vars(inventory)['quantity'] == 10
	
def test_update_ltz_quantity_inventory():
	"""
	GIVEN a Inventory model
	WHEN a Inventory is updated with a quantity field value less than zero
	THEN check the exception raised == FieldConstraintViolation
	"""
	obj = {
		'product_id': "fb9c7029-a328-4c26-8f80-854bf95135c6",
		'store_id': "<UUID_FOR_STORE_T>",
		'quantity': 20,
		'min_stock': 10
	}
	from models.inventory import Inventory
	inventory = Inventory(obj)
	try:
		inventory.update({'quantity': -1})
	except Exception as ex:
		assert ex.args[0] == "FieldConstraintViolation"

def test_update_ltz_min_stock_inventory():
	"""
	GIVEN a Inventory model
	WHEN a Inventory is updated with a min_stock field value less than zero
	THEN check the exception raised == FieldConstraintViolation
	"""
	obj = {
		'product_id': "fb9c7029-a328-4c26-8f80-854bf95135c6",
		'store_id': "<UUID_FOR_STORE_T>",
		'quantity': 20,
		'min_stock': 10
	}
	from models.inventory import Inventory
	inventory = Inventory(obj)
	try:
		inventory.update({'min_stock': -1})
	except Exception as ex:
		assert ex.args[0] == "FieldConstraintViolation"

def test_update_wrong_type_inventory():
	"""
	GIVEN a Inventory model
	WHEN a Inventory is updated with a wrong type field
	THEN check the exception raised == WrongDataType
	"""
	obj = {
		'product_id': "fb9c7029-a328-4c26-8f80-854bf95135c6",
		'store_id': "<UUID_FOR_STORE_T>",
		'quantity': 20,
		'min_stock': 10
	}
	from models.inventory import Inventory
	inventory = Inventory(obj)
	try:
		inventory.update({'store_id': 86})
	except Exception as ex:
		assert ex.args[0] == "WrongDataType"