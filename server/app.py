from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/', )
def hello_world():
    json_data = request.get_json()
    name = json_data['name']
    data = {
        'name' : name,
    }
    account = mongo.db.account.insert(data)
    return jsonify({'result': "OK"})

import eth