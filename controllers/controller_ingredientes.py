


from flask import render_template
from app import app
from models.ingredientes import Ingredientes


@app.route('/ingredientes')
def productos():
    ingredientes_lista = Ingredientes.query.all()  # Obtener todos los productos de la tabla Productos
    return render_template('ingredientes.html', ingredientes=ingredientes_lista)
