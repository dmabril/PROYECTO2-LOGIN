


from flask import render_template
from app import app
from models.productos import Productos  


@app.route('/productos')
def productos():
    productos_lista = Productos.query.all()  # Obtener todos los productos de la tabla Productos
    return render_template('productos.html', productos=productos_lista)
