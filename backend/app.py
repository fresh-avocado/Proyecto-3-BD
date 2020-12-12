from flask import Flask, jsonify, request, flash
from flask_cors import CORS, cross_origin
from p2 import knn_h, knn_r, crear_insertar
import json
import os
import time

# configuration
UPLOAD_FOLDER = './uploads/'
QUERY_FOLDER = './query/'
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

@app.route('/')
def home():
    return '¡Bienvenido Profesor Heider!'

@app.route('/queryImages', methods=['GET'])
@cross_origin()
def query_images():
    query = request.files['image']
    k = request.args.get('k')

    file.save(os.path.join(app.config['QUERY_FOLDER'], query.filename))

    start = int(round(time.time() * 1000))
    result = knn_r("query/" + query.filename, int(k))
    result = [
        {id: 1, name: 'image1'},
        {id: 2, name: 'image2'},
        {id: 3, name: 'image3'},
        {id: 4, name: 'image4'},
        {id: 5, name: 'image5'},
    ]
    end = int(round(time.time() * 1000))

    #knn_r: con r tree
    #knn_h: secuencial

    return jsonify({'images': result, 'execTime': end-start})

@app.route('/uploadImages', methods=['POST'])
@cross_origin()
def index_images():
    images = request.files.getlist('file')
    for image in images:
        print('image name:', image.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    system("cd uploads && ls *.jpg > ../names.txt && ls *.jpeg > ../names.txt")
    crear_insertar()

if __name__ == '__main__':
    app.run()
