from sqlalchemy.orm import query_expression

from config import db
from models.interfaces import CustomSchema

class Product(db.Model):
	__table__ = db.metadata.tables['product']
	stock = query_expression()

	datatypes = {
		'name': str,
		'description': str,
		'category': str,
		'price': float,
		'sku': str
	}

	mandatory = ('name', 'price', 'sku')

	def __init__(self, obj):
		if not all(key in obj for key in self.mandatory):
			raise Exception('MissingKey', 'Required field not found.')
		
		if not all(isinstance(obj[key], type) for key,type in self.datatypes.items()):
			raise Exception('WrongDataType', 'Field value type mismatch.')
		
		if obj['price'] < 0:
			raise Exception('FieldConstraintViolation', 'Price field value can\'t be less than zero.')

		self.name = obj['name']
		self.description = obj['description'] if 'description' in obj else None
		self.category = obj['category'] if 'category' in obj else None
		self.price = obj['price']
		self.sku = obj['sku']
	
	def update(self, obj):
		if not all(isinstance(obj[key], type) if key in obj else True for key,type in self.datatypes.items()):
			raise Exception('WrongDataType', 'Field value type mismatch.')
		
		if 'price' in obj and obj['price'] < 0:
			raise Exception('FieldConstraintViolation', 'Price field value can\'t be less than zero.')
		
		for key in obj.keys():
			if key in vars(self).keys():
				setattr(self, key, obj[key])


class ProductSchema(CustomSchema):
	class Meta:
		fields = ['id', 'name', 'description', 'category', 'price', 'sku']