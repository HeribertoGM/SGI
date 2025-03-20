from flask import Blueprint, jsonify
from collections import OrderedDict

from models.product import Product, ProductSchema
from models.inventory import Inventory, InventorySchema
from models.interfaces import JoinedSchema

stores_bp = Blueprint('stores', __name__)

@stores_bp.get('/health')
def health():
	return jsonify({ "ok": True, 'from': "stores" })

@stores_bp.get('/<string:store_id>/inventory')
def store(store_id):
	query = Product.query.join(Inventory, Product.id == Inventory.product_id).add_columns(Inventory)
	query = query.filter_by(store_id=store_id)

	products = query.all()
	schema = JoinedSchema(many=True, joins=OrderedDict([('product', ProductSchema), ('inventory', InventorySchema)]))
	result = schema.dump(products)
	return jsonify({"ok": True, "length": len(result), "data": result})