
/* function consultarProducto(codigo) {
    fetch(`/consultarProducto/${codigo}`, {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Manejar la respuesta del servidor aquí, por ejemplo, actualizar la vista con los datos del producto consultado
        // Por ejemplo, podrías actualizar el HTML de la página con los datos del producto
        document.getElementById('codigo').value = data.codigo;
        document.getElementById('nombre').value = data.nombre;
        document.getElementById('precio').value = data.precio;
        document.getElementById('cbCategoria').value = data.categoria;
        // No estoy seguro de qué hacer con la imagen, ya que no parece que estés devolviendo una URL de imagen en la respuesta JSON
    })
    .catch(error => {
        console.error('Error:', error);
    });
} */



function editarProducto() {
    const codigo = document.getElementById('codigo').value;
    const nombre = document.getElementById('nombre').value;
    const precio = document.getElementById('precio').value;
    const categoria = document.getElementById('cbCategoria').value;
    const foto = base64url;

    const formData = new FormData();
    formData.append('codigo', codigo);
    formData.append('nombre', nombre);
    formData.append('precio', precio);
    formData.append('cbCategoria', categoria);
    formData.append('fileFoto', foto);

    fetch('/editarProducto', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Manejar la respuesta del servidor
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}




function editarProducto() {
    // Obtener los datos del formulario
    const producto={
        codigo: codigo.value,
        nombre: nombre.value,
        precio: precio.value,
        categoria: cbCategoria.value
    
    }

    const foto = {
        foto: base64url 
    } // Esta es la imagen en formato base64 obtenida del archivo seleccionado PROFRESOR

    const datos = {

        producto:producto,
        foto:foto
    }

    fetch('/editarProducto', {
        method: 'PUT',
        body: JSON.stringify(datos),
        headers:{
            "Content-Type": "application/json",
        },
    })
    .then(response => response.json())
    .then(resultado  =>{
        console.log(resultado)    
        if (resultado.estado) {
            formEditProducto.reset()
            swal.fire("Editar Producto", resultado.mensaje, "success")
        } else {
            swal.fire("Editar Producto", resultado.mensaje, "warning")
        }
    });

}




