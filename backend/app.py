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

@app.route('/queryImages', methods=['POST'])
@cross_origin()
def query_images():
    query = request.files['file']
    k = request.args.get('k')

    query.save(os.path.join(app.config['QUERY_FOLDER'], query.filename))

    start = int(round(time.time() * 1000))
    result = knn_r("query/" + query.filename, int(k))
    end = int(round(time.time() * 1000))

    #knn_r: con r tree
    #knn_h: secuencial

    print('Restult: ')
    print(result)
    return jsonify({'images': result, 'execTime': end-start})

@app.route('/uploadImages', methods=['POST'])
@cross_origin()
def index_images():
    print(request.files)
    images = request.files.getlist('files')
    nombres = open('names.txt', 'w');
    for file in images:
        print('image name:', file.filename)
        nombres.write(file.filename)
        nombres.write('\n')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    nombres.close()
    
    start = int(round(time.time() * 1000))
    crear_insertar()
    end = int(round(time.time() * 1000))

    return jsonify({'execTime': end-start})

@app.route('/reset', methods=['GET'])
@cross_origin()
def reset():
    os.system("rm -rf ./uploads/* && rm rtree.dat rtree.idx nombres.txt names.txt")
    return 'Heider :)'

if __name__ == '__main__':
    app.run()

