#categoriasControler.py
from app import categorias, app
from flask import jsonify
from bson.json_util import dumps

@app.route('/obtenerCategorias')
def obtenerCategorias():
    try:
        cat = categorias.find()
        listaCategorias = list(cat)
        json_data = dumps(listaCategorias)
        retorno = {'categorias': json_data}
        return jsonify(retorno)
    except Exception as e:
        return jsonify({'error': str(e)})



