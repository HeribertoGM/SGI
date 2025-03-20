from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os
import importlib

db = SQLAlchemy()
ma = Marshmallow()

blueprints = {
	'products': {
		'path': 'project.products',
		'name': 'products_bp',
		'url_prefix': '/products'
	},
	'stores': {
		'path': 'project.stores',
		'name': 'stores_bp',
		'url_prefix': '/stores'
	},
	'inventory': {
		'path': 'project.inventory',
		'name': 'inventory_bp',
		'url_prefix': '/inventory'
	}
}

def not_found(err):
	return jsonify({"ok": False, "error": "404 - Not Found", "msg": "The requested URL was not found on the server."}), 404

def create_app():
	load_dotenv()

	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
	app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

	modules = os.getenv("MODULES")[1:-1].replace("'", "").split(',')

	init_extensions(app)
	register_blueprints(app, modules)

	app.register_error_handler(404, not_found)

	return app

def init_extensions(app):
	db.init_app(app)
	ma.init_app(app)

	with app.app_context():
		db.reflect()

def register_blueprints(app, modules):
	for module in modules:
		bp_data = blueprints[module]
		bp = getattr(importlib.import_module(bp_data['path']), bp_data['name'])
		app.register_blueprint(bp, url_prefix=bp_data['url_prefix'] if len(modules) != 1 else None)
