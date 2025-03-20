from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.orm import with_expression

from config import db
from models.product import Product, ProductSchema
from models.inventory import Inventory

products_bp = Blueprint('products', __name__)

@products_bp.get('/health')
def health():
	return jsonify({ "ok": True, 'from': "products"  })

@products_bp.get('/')
def list():
	stock_expr = func.coalesce(func.sum(Inventory.quantity),0)
	query = Product.query.outerjoin(Inventory, Product.id == Inventory.product_id).group_by(Product.id).options(with_expression(Product.stock, stock_expr))
	
	if request.args.get('category') != None:
		query = query.filter(Product.category == request.args.get('category'))
	
	if request.args.get('sku') != None:
		query = query.filter(Product.sku == request.args.get('sku'))

	if request.args.get('minPrice') != None:
		query = query.filter(Product.price >= request.args.get('minPrice'))

	if request.args.get('maxPrice') != None:
		query = query.filter(Product.price <= request.args.get('maxPrice'))
	
	if request.args.get('minStock') != None:
		query = query.having(stock_expr >= request.args.get('minStock'))

	if request.args.get('maxStock') != None:
		query = query.having(stock_expr <= request.args.get('maxStock'))

	count = query.count()

	column_keys = tuple(filter(lambda key: not key.startswith('_'), vars(Product).keys()))
	order_key = vars(Product)['sku']
	if request.args.get('orderBy') != None and request.args.get('orderBy') in column_keys:
		order_key = stock_expr if request.args.get('orderBy') == 'stock' else vars(Product)[request.args.get('orderBy')]

	query = query.order_by(order_key)

	page = int(request.args.get('page')) if request.args.get('page') != None else 0
	per_page = int(request.args.get('perPage')) if request.args.get('perPage') != None else 10
	query = query.limit(per_page).offset(page*per_page)

	products = query.all()
	schema = ProductSchema(many=True, include=('stock',))
	result = schema.dump(products)
	return jsonify({"ok": True, "total": count, "length": len(result), "data": result})

@products_bp.post('/')
def new():
	new_product = None
	try:
		new_product = Product(request.json)
	except Exception as ex:
		return jsonify({"ok": False, "error": ex.args[0], "msg": ex.args[1], "payload": request.json})

	try:
		db.session.add(new_product)
		db.session.commit()
	except Exception as ex:
		return jsonify({"ok": False, "error": type(ex).__name__, "msg": str(ex), "payload": request.json})

	schema = ProductSchema()
	data = schema.dump(new_product)
	return jsonify({"ok": True, "data": data, "payload": request.json})

@products_bp.get('/<uuid:product_id>')
def detail(product_id):
	try:
		query = Product.query.filter(Product.id == product_id)
		product = query.one()
		schema = ProductSchema()
		result = schema.dump(product)

		return jsonify({"ok": True, "data": result, "payload": {"product_id": product_id}})
	except Exception as ex:
		return jsonify({"ok": False, "error": type(ex).__name__, "msg": str(ex), "payload": {"product_id": product_id}})

@products_bp.put('/<uuid:product_id>')
def update(product_id):
	payload = request.json
	payload['product_id'] = product_id
	product = None
	try:
		query = Product.query.filter(Product.id == product_id)
		product = query.one()
	except Exception as ex:
		return jsonify({"ok": False, "error": type(ex).__name__, "msg": str(ex), "payload": payload})
	
	try:
		product.update(request.json)
		db.session.commit()
	except Exception as ex:
		if ex.args[0] in ["WrongDataType", "FieldConstraintViolation"]:
			return jsonify({"ok": False, "error": ex.args[0], "msg": ex.args[1], "payload": payload})
		else:
			return jsonify({"ok": False, "error": type(ex).__name__, "msg": str(ex), "payload": payload})

	schema = ProductSchema()
	data = schema.dump(product)
	return jsonify({"ok": True, "data": data, "payload": payload})

@products_bp.delete('/<uuid:product_id>')
def remove(product_id):
	product = None
	try:
		query = Product.query.filter(Product.id == product_id)
		product = query.one()
	except Exception as ex:
		return jsonify({"ok": False, "error": type(ex).__name__, "msg": str(ex), "payload": {"product_id": product_id}})

	try:
		db.session.delete(product)
		db.session.commit()
	except Exception as ex:
		return jsonify({"ok": False, "error": type(ex).__name__, "msg": str(ex), "payload": {"product_id": product_id}})

	schema = ProductSchema()
	data = schema.dump(product)
	return jsonify({"ok": True, "data": data, "payload": {"product_id": product_id}})
