from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "rahasia"
app.config["MONGO_URI"] = "mongodb://localhost/27017/puskesmas"
mongo = PyMongo(app)