from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

#app = Flask(__name__)
app = Flask(__name__, static_folder="../crypto-currency-exchange-frontend/build", static_url_path="")
app.secret_key = "super secret ke!"
CORS(app)
mongo = PyMongo(app)

import view
