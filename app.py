#app.py

from flask import Flask
import pymongo



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/img'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



miConexion = pymongo.MongoClient('mongodb://localhost:27017')
baseDatos = miConexion['CrudFlask']

productos = baseDatos['productos']
categorias = baseDatos['CATEGORIAS']
usuarios = baseDatos['usuarios']

from controlador.productosControler import *
from controlador.categoriasControler import *
from controlador.loginControler import *

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
