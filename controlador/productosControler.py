# productosControler.py

import os
from bson.objectid import ObjectId
import pymongo
from PIL import Image
from io import BytesIO
import base64
from flask import render_template, request, jsonify, redirect, url_for, session, flash
from app import app, productos, categorias, usuarios
from bson.json_util import dumps
from bson import ObjectId
from flask import jsonify
from bson import json_util





""" @app.route("/listaProductos", methods=['GET', 'POST'])
def listaProductos():
    mensaje_producto_agregado = request.args.get('mensaje_producto_agregado', None)  # Obtener el mensaje de producto agregado de la consulta
    mensaje_inicio_sesion = request.args.get('mensaje_inicio_sesion', None)  # Obtener el mensaje de inicio de sesión de la consulta
    estado = request.args.get('estado', False) 
    if 'usuario' in session:
        listaProductos = productos.find()
        listaCategorias = categorias.find()
        listaP = []
        for p in listaProductos:
            categoria = categorias.find_one({'_id': p['categoria']})
            if categoria:
                p['categoria'] = categoria['nombre']
            else:
                p['categoria'] = "Sin categoría"
            listaP.append(p)
        return render_template('listaProductos.html', productos=listaP, listaCategorias=listaCategorias, mensaje_producto_agregado=mensaje_producto_agregado, mensaje_inicio_sesion=mensaje_inicio_sesion, estado=estado)        
    else:
        return redirect(url_for('login'))  # Redirigir al formulario de inicio de sesión si el usuario no está autenticado
 """


@app.route("/listaProductos", methods=['GET', 'POST'])
def listaProductos():
    mensaje_producto_agregado = request.args.get('mensaje_producto_agregado', None)  # Obtener el mensaje de producto agregado de la consulta
    mensaje_inicio_sesion = request.args.get('mensaje_inicio_sesion', None)  # Obtener el mensaje de inicio de sesión de la consulta
    estado = request.args.get('estado', False) 

    if 'usuario' in session:
        # Si el usuario ha iniciado sesión, se muestran los productos
        listaProductos = productos.find()
        listaCategorias = categorias.find()
        listaP = []
        for p in listaProductos:
            categoria = categorias.find_one({'_id': p['categoria']})
            if categoria:
                p['categoria'] = categoria['nombre']
            else:
                p['categoria'] = "Sin categoría"
            listaP.append(p)

        # Si hay un mensaje de inicio de sesión en la sesión, se elimina
        if 'mensaje_inicio_sesion' in session:
            session.pop('mensaje_inicio_sesion')

        # Se renderiza la plantilla de lista de productos
        return render_template('listaProductos.html', productos=listaP, listaCategorias=listaCategorias, mensaje_producto_agregado=mensaje_producto_agregado, mensaje_inicio_sesion=mensaje_inicio_sesion, estado=estado)        
    else:
        # Si el usuario no ha iniciado sesión, se redirige al formulario de inicio de sesión
        return redirect(url_for('login'))




@app.route('/vistaAgregarProducto', methods=['GET'])
def vistaAgregarProducto():
    categoriasBD = categorias.find()
    return render_template('formAgregarProd.html', categorias=categoriasBD)




@app.route('/agregarProducto', methods=['POST'])
def agregarProducto():
    mensaje = None
    estado = False
    try:
        #datos traidos del formulario
        codigo = int(request.form['codigo'])
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        idCategoria = ObjectId(request.form['cdCategoria'])
        foto = request.files['fileFoto'] 
        #producto tipo diccionario
        producto = {
            'codigo': codigo,
            'nombre': nombre,
            'precio': precio,
            'categoria': idCategoria
        }
        #Insertar producto creado en base de datos
        resultado = productos.insert_one(producto)
        # acknowledged,  valida que se halla insertado en la BD MONGO
        if (resultado.acknowledged):
            idProducto = resultado.inserted_id # genera el id unico en el producto insertado
            nombreFotos = f'{idProducto}.jpg'
            #.save() metodo para guardar la imagen adjunta en el sistema de archivos del servidor
            #os.path.join(): Este es un método del módulo os en Python que se utiliza para unir componentes de ruta en una cadena de ruta. En este caso, se utiliza para concatenar la ruta del directorio de carga (UPLOAD_FOLDER) con el nombre del archivo (nombreFotos), 
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFotos))
            mensaje = 'Producto Agregado Correctamente'
            estado = True
        else:
            mensaje = 'Problema Al Agregar El Producto'
    except pymongo.errors.PyMongoError as error:  
        mensaje = str(error)
    return redirect(url_for('listaProductos', mensaje_producto_agregado=mensaje, estado=estado))




@app.route('/agregarProductoJson', methods=['POST'])
def agregarProductoJson():
    # Inicializar variables para el estado y el mensaje de la operación
    estado = False
    mensaje = None
    
    try:
        # Recibe los datos en formato JSON desde la solicitud
        datos = request.json
        
        # Extrae los datos del producto y la foto del JSON recibido
        producto = datos.get('producto')
        fotoBase64 = datos.get('foto')["foto"]
        
        # Crea un diccionario con los datos del producto
        producto = {
            'codigo': int(producto["codigo"]),
            'nombre': producto["nombre"],
            'precio': int(producto["precio"]),
            'categoria': ObjectId(producto["categoria"])
        }
        
        # Inserta el producto en la base de datos MongoDB
        resultado = productos.insert_one(producto)
        
        # Verifica si la inserción fue exitosa
        if resultado.acknowledged:
            # Define la ruta donde se guardará la imagen del producto
            rutaImagen = f"{os.path.join(app.config['UPLOAD_FOLDER'])}/{resultado.inserted_id}.jpg"
            
            # Extrae la parte base64 de la imagen recibida y la decodifica
            fotoBase64 = fotoBase64[fotoBase64.index(',') + 1]
            fotoDecodificada = base64.b64decode(fotoBase64)
            
            # Abre la imagen decodificada y la guarda en formato JPEG en la ruta especificada
            imagen = Image.open(BytesIO(fotoDecodificada))
            imagenJpg = imagen.convert('RGB')
            imagen.save(rutaImagen)
            
            # Actualiza el estado y el mensaje de la operación
            estado = True
            mensaje = 'Producto Agregado correctamente'
        else:
            # Actualiza el mensaje si hubo problemas al agregar el producto
            mensaje = 'Problemas al Agregar'
    except pymongo.errors.PyMongoError as error:
        # Captura cualquier excepción de PyMongo y actualiza el mensaje
        mensaje = str(error)
    
    # Retorna la respuesta en formato JSON con el estado y el mensaje de la operación
    retorno = {"estado": estado, "mensaje": mensaje}
    return jsonify(retorno)




@app.route('/obtenerProductos')
def obtenerProductos():
    try:
        prods = productos.find()
        listaProductos = list(prods)
        json_data = dumps(listaProductos)
        retorno = {'productos': json_data}
        return jsonify(retorno)
    except Exception as e:
        return jsonify({'error': str(e)})
    


    
@app.route('/consultarProducto/<codigo>', methods=['GET'])
def consultarProducto(codigo):
    estado = False
    mensaje = None
    producto = None
    listaCategorias = None  # Define listaCategorias fuera del bloque try para que esté disponible en caso de excepción
    try:
        datosConsulta = {"codigo": int(codigo)}
        producto = productos.find_one(datosConsulta)
        if producto:
            estado = True
        listaCategorias = categorias.find()  # Mueve esta línea dentro del bloque try
    except pymongo.errors.PyMongoError as error:
        mensaje = error

    return render_template('formEditarProd.html', producto=producto, categorias=listaCategorias)




@app.route("/editarProducto", methods=["POST"])
def editarProducto():
    estado = False
    mensajeEditProd = None
    try:
        codigo = int(request.form['codigo'])
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        idCategoria = ObjectId(request.form['cbCategoria'])
        foto = request.files['fileFoto']
        idProducto = ObjectId(request.form['idProducto'])
        producto = {
            'codigo': codigo,
            'nombre': nombre,
            'precio': precio,
            'categoria': idCategoria
        }
        #actualizar BD en base al id

        resultado = productos.update_one({'_id': idProducto}, {"$set": producto})
        # acknowledged que indica si el servidor de MongoDB confirmó que recibió y procesó la operación de escritura.
        if resultado.acknowledged:

            if (foto):
                nombreFoto = f"{idProducto}.jpg"
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFoto))
            mensajeEditProd = "actualizado correctamente"
            estado=True
        else:
            mensajeEditProd = "problemas al actualizar"

    except pymongo.errors as error:
        mensajeEditProd = error

    return render_template("formEditarProd.html", producto=producto, mensajeEditProd=mensajeEditProd, estado=estado)






@app.route('/eliminarProducto/<_id>', methods=['DELETE'])
def eliminarProducto(_id):
    
    try:
        result = productos.delete_one({'_id': ObjectId(_id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'Producto eliminado correctamente'}), 200
        else:
            return jsonify({'message': 'El producto no existe'}), 404
    except pymongo.errors.PyMongoError as error:
        return render_template('listaProductos.html')

