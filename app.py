
from models import db  
from flask import Flask, render_template, redirect,url_for
from models.heladeria import Heladeria
from models.productosingredientes import Productosingredientes
from models.productos import Productos
from models.ingredientes import Ingredientes
from funciones import validacion_sano, costo_produccion_producto,producto_mas_rentable,abastecer


# Inicializamos la base de datos
app = Flask(__name__, template_folder='views')

# Configuración de la base de datos BD_Heladeria
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BD_Heladeria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos la base de datos
db.init_app(app)

# Ruta principal
@app.route('/')
def index():
    # Consultar todos los modelos para la vista principal
    heladeria = Heladeria.query.all()
    productosingredientes = Productosingredientes.query.all()
    productos = Productos.query.all()
    ingredientes = Ingredientes.query.all()

    # Renderizamos la plantilla principal y pasamos los datos
    return render_template('index.html', 
                           heladeria=heladeria, 
                           productosingredientes=productosingredientes,
                           productos=productos,
                           ingredientes=ingredientes
                           )

# Ruta para ver heladerías
@app.route('/Heladeria')
def heladeria_view():
    # Consultar todas las heladerías
    heladeria = Heladeria.query.all()
    return render_template('heladeria.html', heladeria=heladeria)

# Ruta para ver productos e ingredientes
@app.route('/Productosingredientes')

#def productosingredientes_view():
#    # Consultar todas las relaciones entre productos e ingredientes
#    productosingredientes_lista = Productosingredientes.query.all()  
#    return render_template('productosingredientes.html', productosingredientes=productosingredientes_lista)

def productosingredientes_view():
    # Consultar todas las relaciones entre productos e ingredientes
    productosingredientes_lista = Productosingredientes.query.all()

    # Crear un diccionario para almacenar los costos de producción de cada producto
    costos = {}
    
    for item in productosingredientes_lista:
        # Obtener el costo de producción de cada producto relacionado
        costo = costo_produccion_producto(item.id_producto)
        costos[item.id_producto] = costo

    producto_rentable, rentabilidad = producto_mas_rentable()

    return render_template('productosingredientes.html', 
                           productosingredientes=productosingredientes_lista, 
                           costos=costos,
                           producto_rentable=producto_rentable,
                           rentabilidad=rentabilidad)


@app.route('/productos')
def productos_view():
    # Consultar todas las relaciones entre productos e ingredientes
    productos_lista = Productos.query.all()  
    return render_template('productos.html', productos=productos_lista)
"""
@app.route('/ingredientes')
def ingredientes_view():
    # Consultar todas las relaciones entre productos e ingredientes
    ingredientes_lista = Ingredientes.query.all()  
    return render_template('ingredientes.html', ingredientes=ingredientes_lista)
"""    
@app.route('/ingredientes')
def ingredientes_view():
    # Consultar todas las relaciones entre productos e ingredientes
    ingredientes_lista = Ingredientes.query.all()

    # Pasamos la lista de ingredientes y la función validacion_sano a la plantilla
    return render_template('ingredientes.html', ingredientes=ingredientes_lista, validacion_sano=validacion_sano)


@app.route('/abastecer/<int:id_ingrediente>', methods=['POST'])
def abastecer_ingrediente(id_ingrediente):
    # Buscar el ingrediente en la base de datos
    ingrediente = Ingredientes.query.get(id_ingrediente)
    
    if ingrediente:
        # Llamamos a la función abastecer para aumentar el inventario
        nuevo_inventario = abastecer(ingrediente.tipo_ingrediente, ingrediente.inventario)
        ingrediente.inventario = nuevo_inventario
        
        # Guardamos los cambios en la base de datos
        db.session.commit()

    # Redirigir a la vista de ingredientes
    return redirect(url_for('ingredientes_view'))

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)


# Inicializar la base de datos con datos predeterminados
if __name__ == '__main__':
    # Crear la base de datos si no existe
    with app.app_context():
        # Asegura que las tablas sean creadas
        db.drop_all()  # Comment this line in production
        db.create_all()  # Esto crea las tablas si no existen

        # Insertar datos iniciales si no existen en la tabla Heladeria
        if not Heladeria.query.first():
            heladeria_iniciales = [
                Heladeria(id_heladeria=1, nombre="PYTHON ICE CREAM", direccion="Calle 123 # 00-00", telefono="9999999")
            ]
            db.session.add_all(heladeria_iniciales)
            db.session.commit()

        
        if not Productos.query.first():
            productos_iniciales = [
                Productos(id_producto=1, nombre="Samurai de fresas", precio=4900, tipo_vaso="Vaso Ecologico", volumen=52.00, tipo_producto="Copa"),
                Productos(id_producto=2, nombre="Samurai de mandarinas", precio=2500, tipo_vaso="Vaso Ecologico", volumen=80.00, tipo_producto="Copa"),
                Productos(id_producto=3, nombre="Malteda chocoespacial", precio=11000, tipo_vaso="Vaso Plastico", volumen=100.00, tipo_producto="Malteada"),
                Productos(id_producto=4, nombre="Cupihelado", precio=3200, tipo_vaso="Vaso Ecologico", volumen=52.00, tipo_producto="Copa")
            ]
            db.session.add_all(productos_iniciales)
            db.session.commit()

        if not Ingredientes.query.first():
            ingredientes_iniciales = [
                #Bases
                Ingredientes(id_ingrediente=1, nombre="Helado de Fresa", precio=1200, numero_calorias=300,es_vegetarianos=1,sabor="Fresa", tipo_ingrediente= "Base",inventario=50.0),
                Ingredientes(id_ingrediente=2, nombre="Helado de Mandarina", precio=1200, numero_calorias=280,es_vegetarianos=1,sabor="Mandarina", tipo_ingrediente= "Base",inventario=50.0),
                Ingredientes(id_ingrediente=3, nombre="Helado de Chocolate", precio=1500, numero_calorias=400,es_vegetarianos=0,sabor="Chocolate", tipo_ingrediente= "Base",inventario=50.0),
                Ingredientes(id_ingrediente=4, nombre="Helado de Vainilla", precio=1200, numero_calorias=300,es_vegetarianos=0,sabor="Vainilla", tipo_ingrediente= "Base",inventario=50.0),
                
                #Complementos
                Ingredientes(id_ingrediente=5, nombre="Chispas de chocolate", precio=500, numero_calorias=500,es_vegetarianos=0,sabor="", tipo_ingrediente= "Complemento",inventario=50.0),
                Ingredientes(id_ingrediente=6, nombre="Mani Japonés", precio=900, numero_calorias=200,es_vegetarianos=1,sabor="", tipo_ingrediente= "Complemento",inventario=50.0),
                Ingredientes(id_ingrediente=7, nombre="Chantilli", precio=800, numero_calorias=300,es_vegetarianos=0,sabor="", tipo_ingrediente= "Complemento",inventario=50.0),
                Ingredientes(id_ingrediente=8, nombre="Galletas", precio=1000, numero_calorias=430,es_vegetarianos=0,sabor="", tipo_ingrediente= "Complemento",inventario=50.0),
                Ingredientes(id_ingrediente=9, nombre="Leche", precio=700, numero_calorias=50,es_vegetarianos=0,sabor="", tipo_ingrediente= "Complemento",inventario=50.0),
                Ingredientes(id_ingrediente=10, nombre="Trozos Mandarina", precio=200, numero_calorias=10,es_vegetarianos=1,sabor="", tipo_ingrediente= "Complemento",inventario=50.0),
                Ingredientes(id_ingrediente=11, nombre="Trozos Cereza", precio=200, numero_calorias=10,es_vegetarianos=1,sabor="", tipo_ingrediente= "Complemento",inventario=50.0)
                
                

            ]
            db.session.add_all(ingredientes_iniciales)
            db.session.commit()




        # Insertar datos iniciales si no existen en la tabla Productosingredientes
        if not Productosingredientes.query.first():
            productosingredientes_iniciales = [
                #Producto 1
                Productosingredientes(id_heladeria=1,id_producto=1,id_ingrediente=1), 
                Productosingredientes(id_heladeria=1,id_producto=1,id_ingrediente=8), 
                Productosingredientes(id_heladeria=1,id_producto=1,id_ingrediente=9), 

                #Producto 2
                Productosingredientes(id_heladeria=1,id_producto=2,id_ingrediente=2),
                Productosingredientes(id_heladeria=1,id_producto=2,id_ingrediente=7),
                Productosingredientes(id_heladeria=1,id_producto=2,id_ingrediente=10),


                #Producto 3
                Productosingredientes(id_heladeria=1,id_producto=3,id_ingrediente=3),
                Productosingredientes(id_heladeria=1,id_producto=3,id_ingrediente=9),
                Productosingredientes(id_heladeria=1,id_producto=3,id_ingrediente=5),

                #Producto 4
                Productosingredientes(id_heladeria=1,id_producto=4,id_ingrediente=4),
                Productosingredientes(id_heladeria=1,id_producto=4,id_ingrediente=11),
                Productosingredientes(id_heladeria=1,id_producto=4,id_ingrediente=6)


            ]
            db.session.add_all(productosingredientes_iniciales)
            db.session.commit()

    # Ejecutar la aplicación
    app.run(debug=True)
