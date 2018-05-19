from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)
CORS(app)
Session(app)
mongo = PyMongo(app)

@app.route('/', )
def hello_world():
    return jsonify({'result': "OK"})

import view
import tr