from flask import Flask, jsonify, request, flash
from flask_cors import CORS, cross_origin
import json
import os
import time

# configuration
UPLOAD_FOLDER = './uploads/'
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

@app.route('/')
def home():
    return '¡Bienvenido Profesor Heider!'

if __name__ == '__main__':
    app.run()
