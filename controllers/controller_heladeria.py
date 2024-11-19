


from flask import render_template
from app import app
from models.heladeria import Heladeria  


@app.route('/heladeria')
def productos():
    Heladeria_lista = Heladeria.query.all()  # Obtener todos los productos de la tabla Productos
    return render_template('heladeria.html', Heladeria=Heladeria_lista)
