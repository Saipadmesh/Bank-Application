import json
from unicodedata import name
from flask import current_app, g, jsonify, request
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy

from bson.json_util import dumps
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db():
    """
    Return Database instance
    """
    db = getattr(g,"_database",None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    
    return db

db = LocalProxy(get_db)

def get_users():
    """
    Get list of users
    """
    records = db.users.find()
    return dumps(records)

def add_user(_json):
    """
    Add a new user
    """
    _name = _json.get('name')
    _email = _json.get('email')
    _pwd = _json.get('pwd')
    if _name and _email and _pwd and request.method == 'POST':
        record = {'name': _name,'email':_email,'pwd':_pwd,'isAdmin':False}
        id = db.users.insert_one(record)
        resp = jsonify("User added successfully")
        resp.status_code = 200
    else:
        resp = jsonify("Invalid Arguments")
        resp.status_code = 400
    return resp
