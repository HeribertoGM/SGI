
def test_create_correct_transfer_transfer():
	"""
	GIVEN a Transfer model
	WHEN a new "TRANSFER" type Transfer is created
	THEN check the product_id, source_store_id, target_store_id, quantity and type are defined correctly
	"""
	obj = {
		'product_id': "0bcb2354-db55-4359-9601-fb62884c06c7",
		'source_store_id': "<UUID_FOR_STORE_T1>",
		'target_store_id': "<UUID_FOR_STORE_T2>",
		'quantity': 10,
		'type': 'TRANSFER'
	}
	from models.transfer import Transfer
	transfer = Transfer(obj)
	assert vars(transfer)['product_id'] == obj['product_id']
	assert vars(transfer)['source_store_id'] == obj['source_store_id']
	assert vars(transfer)['target_store_id'] == obj['target_store_id']
	assert vars(transfer)['quantity'] == obj['quantity']
	assert vars(transfer)['type'] == obj['type']

def test_create_correct_in_transfer():
	"""
	GIVEN a Transfer model
	WHEN a new "IN" type Transfer is created
	THEN check the product_id, target_store_id, quantity and type are defined correctly
	"""
	obj = {
		'product_id': "0bcb2354-db55-4359-9601-fb62884c06c7",
		'target_store_id': "<UUID_FOR_STORE_T2>",
		'quantity': 10,
		'type': 'IN'
	}
	from models.transfer import Transfer
	transfer = Transfer(obj)
	assert vars(transfer)['product_id'] == obj['product_id']
	assert vars(transfer)['target_store_id'] == obj['target_store_id']
	assert vars(transfer)['quantity'] == obj['quantity']
	assert vars(transfer)['type'] == obj['type']

def test_create_correct_out_transfer():
	"""
	GIVEN a Transfer model
	WHEN a new "OUT" type Transfer is created
	THEN check the product_id, source_store_id, quantity and type are defined correctly
	"""
	obj = {
		'product_id': "0bcb2354-db55-4359-9601-fb62884c06c7",
		'source_store_id': "<UUID_FOR_STORE_T1>",
		'quantity': 10,
		'type': 'OUT'
	}
	from models.transfer import Transfer
	transfer = Transfer(obj)
	assert vars(transfer)['product_id'] == obj['product_id']
	assert vars(transfer)['source_store_id'] == obj['source_store_id']
	assert vars(transfer)['quantity'] == obj['quantity']
	assert vars(transfer)['type'] == obj['type']

def test_create_missing_mandatory_field_transfer():
	"""
	GIVEN a Transfer model
	WHEN a new Transfer is created with a missing field
	THEN check the exception raised == MissingKey
	"""
	obj = {
		'product_id': "0bcb2354-db55-4359-9601-fb62884c06c7",
		'source_store_id': "<UUID_FOR_STORE_T1>",
		'target_store_id': "<UUID_FOR_STORE_T2>",
		'quantity': 10,
	}
	try:
		from models.transfer import Transfer
		transfer = Transfer(obj)
	except Exception as ex:
		assert ex.args[0] == "MissingKey"

def test_create_missing_transfer_conditional_field_transfer():
	"""
	GIVEN a Transfer model
	WHEN a new "TRANSFER" Transfer is created with a missing conditional field
	THEN check the exception raised == MissingKey
	"""
	obj = {
		'product_id': "0bcb2354-db55-4359-9601-fb62884c06c7",
		'source_store_id': "<UUID_FOR_STORE_T1>",
		'quantity': 10,
		'type': "TRANSFER"
	}
	try:
		from models.transfer import Transfer
		transfer = Transfer(obj)
	except Exception as ex:
		assert ex.args[0] == "MissingKey"

def test_create_missing_in_conditional_field_transfer():
	"""
	GIVEN a Transfer model
	WHEN a new "IN" Transfer is created with a missing conditional field
	THEN check the exception raised == MissingKey
	"""
	obj = {
		'product_id': "0bcb2354-db55-4359-9601-fb62884c06c7",
		'quantity': 10,
		'type': "IN"
	}
	try:
		from models.transfer import Transfer
		transfer = Transfer(obj)
	except Exception as ex:
		assert ex.args[0] == "MissingKey"

def test_create_missing_out_conditional_field_transfer():
	"""
	GIVEN a Transfer model
	WHEN a new "OUT" Transfer is created with a missing conditional field
	THEN check the exception raised == MissingKey
	"""
	obj = {
		'product_id': "0bcb2354-db55-4359-9601-fb62884c06c7",
		'quantity': 10,
		'type': "OUT"
	}
	try:
		from models.transfer import Transfer
		transfer = Transfer(obj)
	except Exception as ex:
		assert ex.args[0] == "MissingKey"

def test_create_wrong_type_transfer():
	"""
	GIVEN a Transfer model
	WHEN a new Transfer is created with a wrong type field
	THEN check the exception raised == WrongDataType
	"""
	obj = {
		'product_id': "0bcb2354-db55-4359-9601-fb62884c06c7",
		'source_store_id': 86,
		'target_store_id': "<UUID_FOR_STORE_T2>",
		'quantity': 10,
		'type': 'TRANSFER'
	}
	try:
		from models.transfer import Transfer
		transfer = Transfer(obj)
	except Exception as ex:
		assert ex.args[0] == "WrongDataType"

def test_create_ltz_quantity_transfer():
	"""
	GIVEN a Transfer model
	WHEN a new Transfer is created with a quantity field value less than zero
	THEN check the exception raised == FieldConstraintViolation
	"""
	obj = {
		'product_id': "0bcb2354-db55-4359-9601-fb62884c06c7",
		'source_store_id': "<UUID_FOR_STORE_T1>",
		'target_store_id': "<UUID_FOR_STORE_T2>",
		'quantity': -1,
		'type': 'TRANSFER'
	}
	try:
		from models.transfer import Transfer
		transfer = Transfer(obj)
	except Exception as ex:
		assert ex.args[0] == "FieldConstraintViolation"

def test_create_wrong_enum_type_transfer():
	"""
	GIVEN a Transfer model
	WHEN a new Transfer is created with a type field value out of enum(IN, OUT, TRANSFER)
	THEN check the exception raised == FieldConstraintViolation
	"""
	obj = {
		'product_id': "0bcb2354-db55-4359-9601-fb62884c06c7",
		'source_store_id': "<UUID_FOR_STORE_T1>",
		'target_store_id': "<UUID_FOR_STORE_T2>",
		'quantity': 10,
		'type': 'TEST'
	}
	try:
		from models.transfer import Transfer
		transfer = Transfer(obj)
	except Exception as ex:
		assert ex.args[0] == "FieldConstraintViolation"

def test_create_same_source_target_transfer():
	"""
	GIVEN a Transfer model
	WHEN a new Transfer is created with the same source and target
	THEN check the exception raised == FieldConstraintViolation
	"""
	obj = {
		'product_id': "0bcb2354-db55-4359-9601-fb62884c06c7",
		'source_store_id': "<UUID_FOR_STORE_T1>",
		'target_store_id': "<UUID_FOR_STORE_T1>",
		'quantity': 10,
		'type': 'TRANSFER'
	}
	try:
		from models.transfer import Transfer
		transfer = Transfer(obj)
	except Exception as ex:
		assert ex.args[0] == "FieldConstraintViolation"