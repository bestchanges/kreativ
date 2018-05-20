from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "super secret ke!"
CORS(app)
mongo = PyMongo(app)

@app.route('/', )
def hello_world():
    return jsonify({'result': "OK"})

import view
import tr