


from flask import render_template
from app import app
from models.productosingredientes import Productosingredientes  


@app.route('/productosingredientes')
def productos():
    Productosingredientes_lista = Productosingredientes.query.all()  # Obtener todos los productos de la tabla Productos
    return render_template('productosingredientes.html', Productosingredientes=Productosingredientes_lista)




