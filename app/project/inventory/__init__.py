from flask import Blueprint, jsonify, request
from collections import OrderedDict

from config import db
from models.product import Product, ProductSchema
from models.inventory import Inventory, InventorySchema
from models.transfer import Transfer
from models.interfaces import JoinedSchema

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.get('/health')
def health():
	return jsonify({ "ok": True, 'from': "inventory" })

@inventory_bp.get('/alerts')
def list():
	query = Product.query.join(Inventory, Product.id == Inventory.product_id).add_columns(Inventory)
	query = query.filter(Inventory.quantity < Inventory.min_stock)

	products = query.all()
	schema = JoinedSchema(many=True, joins=OrderedDict([('product', ProductSchema), ('inventory', InventorySchema)]))
	result = schema.dump(products)
	return jsonify({"ok": True, "length": len(result), "data": result})

@inventory_bp.post('/transfer')
def transfer():
	new_transfer = None
	try:
		new_transfer = Transfer(request.json)
	except Exception as ex:
		return jsonify({"ok": False, "error": ex.args[0], "msg": ex.args[1], "payload": request.json})
	
	source = None
	target = None
	try:
		if new_transfer.type in ['TRANSFER', 'OUT']:
			query = Inventory.query.filter_by(store_id=new_transfer.source_store_id, product_id=new_transfer.product_id)
			source = query.one()

			if getattr(source, 'quantity') < new_transfer.quantity:
				raise Exception('FieldConstraintViolation', 'Not enough stock of product in source store inventory.')
			
		if new_transfer.type in ['TRANSFER', 'IN']:
			query = Inventory.query.filter_by(store_id=new_transfer.target_store_id, product_id=new_transfer.product_id)
			target = query.one_or_none()

			if target == None:
				target = Inventory({
					'store_id': new_transfer.target_store_id,
					'product_id': new_transfer.product_id,
					'quantity': 0,
					'min_stock': 10
				})

	except Exception as ex:
		if ex.args[0] == "FieldConstraintViolation":
			return jsonify({"ok": False, "error": ex.args[0], "msg": ex.args[1], "payload": request.json})
		else:
			return jsonify({"ok": False, "error": type(ex).__name__, "msg": str(ex), "payload": request.json})
		
	try:
		if new_transfer.type in ['TRANSFER', 'OUT']:
			source.update({'quantity': int(source.quantity) - int(new_transfer.quantity)})
		if new_transfer.type in ['TRANSFER', 'IN']:
			target.update({'quantity': int(target.quantity) + int(new_transfer.quantity)})
	except Exception as ex:
		if ex.args[0] in ["WrongDataType", "FieldConstraintViolation"]:
			return jsonify({"ok": False, "error": ex.args[0], "msg": ex.args[1], "payload": request.json})
		else:
			return jsonify({"ok": False, "error": type(ex).__name__, "msg": str(ex), "payload": request.json})

	try:
		if target != None and target.id == None:
			db.session.add(target)
		db.session.add(new_transfer)
		db.session.commit()
	except Exception as ex:
		return jsonify({"ok": False, "error": type(ex).__name__, "msg": str(ex), "payload": request.json})

	schema = InventorySchema()
	data = {}

	if new_transfer.type in ['TRANSFER', 'OUT']:
		data['source'] = schema.dump(source)
	if new_transfer.type in ['TRANSFER', 'IN']:
		data['target'] = schema.dump(target)

	return jsonify({"ok": True, "data": data, "payload": request.json})