from flask import Flask, jsonify, request, flash
from flask_cors import CORS, cross_origin
from p2 import knn_h, knn_r, crear_insertar
from base64 import encodebytes
from PIL import Image
import json
import os
import io
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

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

@app.route('/queryImages', methods=['POST'])
@cross_origin()
def query_images():
    query = request.files['file']
    k = request.args.get('k')

    query.save(os.path.join(app.config['QUERY_FOLDER'], query.filename))

    start = int(round(time.time() * 1000))
    result = knn_r("query/" + query.filename, int(k))
    end = int(round(time.time() * 1000))

    encoded_images = []
    #knn_r: con r tree
    #knn_h: secuencial


    for re in result:
        encoded_images.append({'id': re['id'], 'image': get_response_image('uploads/' + re['name'])})

    # print('Result: ')
    # print(encoded_images)
    # print(result)
    return jsonify({'images': result, 'execTime': end-start})

@app.route('/uploadImages', methods=['POST'])
@cross_origin()
def index_images():
    os.system("rm -rf ./uploads/* && rm -rf ./query/* && rm rtree.dat rtree.idx nombres.txt names.txt")
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
    os.system("rm -rf ./uploads/* && rm -rf ./query/* && rm rtree.dat rtree.idx nombres.txt names.txt")
    return 'Heider :)'

if __name__ == '__main__':
    app.run()

