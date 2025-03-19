from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

db = SQLAlchemy()
ma = Marshmallow()


def not_found(err):
	return jsonify({"ok": False, "error": "404 - Not Found", "msg": "The requested URL was not found on the server."}), 404

def create_app():
	load_dotenv()

	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
	app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

	init_extensions(app)
	register_blueprints(app)

	app.register_error_handler(404, not_found)

	return app

def init_extensions(app):
	db.init_app(app)
	ma.init_app(app)

	with app.app_context():
		db.reflect()

def register_blueprints(app):
	from project.products import bp

	app.register_blueprint(bp)
