from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

engine = create_engine("mysql://root@localhost/flask")
if not database_exists(engine.url):
    create_database(engine.url)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/flask'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(40))
    password = db.Column(db.String(65))
    created_at = db.Column(db.String(40))
    updated_at = db.Column(db.String(40))
    last_login = db.Column(db.String(40))
    token = db.Column(db.String(30))

class Products(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    status = db.Column(db.String(15))