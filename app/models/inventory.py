from config import db
from models.interfaces import CustomSchema

class Inventory(db.Model):
	__table__ = db.metadata.tables['inventory']

	datatypes = {
		'product_id': str,
		'store_id': str,
		'quantity': int,
		'min_stock': int
	}

	mandatory = ('product_id', 'store_id', 'quantity', 'min_stock')

	def __init__(self, obj):
		if not all(key in obj for key in self.mandatory):
			raise Exception('MissingKey', 'Required field not found.')
		
		if not all(isinstance(obj[key], type) for key,type in self.datatypes.items()):
			raise Exception('WrongDataType', 'Field value type mismatch.')
		
		if obj['quantity'] < 0:
			raise Exception('FieldConstraintViolation', 'Quantity field value can\'t be less than zero.')
		if obj['min_stock'] < 0:
			raise Exception('FieldConstraintViolation', 'Min_stock field value can\'t be less than zero.')

		self.product_id = obj['product_id']
		self.store_id = obj['store_id']
		self.quantity = obj['quantity']
		self.min_stock = obj['min_stock']

	def update(self, obj):
		if not all(isinstance(obj[key], type) if key in obj else True for key,type in self.datatypes.items()):
			raise Exception('WrongDataType', 'Field value type mismatch.')
		
		if 'quantity' in obj and obj['quantity'] < 0:
			raise Exception('FieldConstraintViolation', 'Quantity field value can\'t be less than zero.')
		if 'min_stock' in obj and obj['min_stock'] < 0:
			raise Exception('FieldConstraintViolation', 'Min_stock field value can\'t be less than zero.')
		
		for key in obj.keys():
			if key in vars(self).keys():
				setattr(self, key, obj[key])

class InventorySchema(CustomSchema):
	class Meta:
		fields = ['id', 'product_id', 'store_id', 'quantity', 'min_stock']