from config import db
from models.interfaces import CustomSchema
	
class Transfer(db.Model):
	__table__ = db.metadata.tables['transfer']

	datatypes = {
		'product_id': str,
		'source_store_id': str,
		'target_store_id': str,
		'quantity': int,
		'type': str
	}

	mandatory = ('product_id', 'quantity', 'type')

	conditional = {
		'IN': ['target_store_id'],
		'OUT': ['source_store_id'],
		'TRANSFER': ['source_store_id', 'target_store_id']
	}

	def __init__(self, obj):
		if not all(key in obj for key in self.mandatory):
			raise Exception('MissingKey', 'Required field not found.')
		
		if obj['type'] not in ['IN', 'OUT', 'TRANSFER']:
			raise Exception('FieldConstraintViolation', 'Type field value must be one of enum(IN, OUT, TRANSFER).')
		
		if not all(key in obj for key in self.conditional[obj['type']]):
			raise Exception('MissingKey', 'Required field not found.')
		
		if not all(isinstance(obj[key], type) if key in obj else True for key,type in self.datatypes.items()):
			raise Exception('WrongDataType', 'Field value type mismatch.')
		
		if obj['quantity'] < 0:
			raise Exception('FieldConstraintViolation', 'Quantity field value can\'t be less than zero.')
		
		if obj['type'] == 'TRANSFER' and obj['source_store_id'] == obj['target_store_id']:
			raise Exception('FieldConstraintViolation', 'Source_store_id and target_store_id fields must be different.')

		self.product_id = obj['product_id']
		self.source_store_id = obj['source_store_id'] if 'source_store_id' in obj else None
		self.target_store_id = obj['target_store_id'] if 'target_store_id' in obj else None
		self.quantity = obj['quantity']
		self.type = obj['type']

class TransferSchema(CustomSchema):
	class Meta:
		fields = ['id', 'product_id', 'source_store_id', 'target_store_id', 'quantity', 'timestamp', 'type']
