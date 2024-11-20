

from os import system
from models.ingredientes import Ingredientes
from models.productos import Productos
from models.productosingredientes import Productosingredientes


def validacion_sano(numero_calorias, es_vegetariano):
    if numero_calorias < 100 or es_vegetariano:
        return True
    else:
        return False
    
        

def conteo_calorias(self, numero_calorias):
    if not isinstance(numero_calorias, list):  # Verificamos que sea una lista
        raise ValueError("El parámetro 'numero_calorias' debe ser una lista de números.")
    
    # Calculamos la suma de las calorías y aplicamos el factor de reducción
    conteo_calorias_producto = round(sum(numero_calorias) * 0.95, 2)
    
    return conteo_calorias_producto



def costo_produccion_producto(producto_id):
    # Fetch the product based on its ID
    producto = Productos.query.get(producto_id)
    
    if not producto:
        return None  # Handle case where product does not exist
    
    # Start with the price of the product itself
    costo_total = producto.precio
    
    # Fetch all related product-ingredient relationships
    ingredientes_relacionados = Productosingredientes.query.filter_by(id_producto=producto_id).all()
    
    # Add the price of each ingredient to the total cost
    for relacion in ingredientes_relacionados:
        ingrediente = Ingredientes.query.get(relacion.id_ingrediente)
        if ingrediente:
            costo_total += ingrediente.precio
    
    return costo_total


def producto_mas_rentable():
    # Obtener todos los productos
    productos = Productos.query.all()
    
    # Diccionario para almacenar la rentabilidad de cada producto
    rentabilidad = {}
    
    for producto in productos:
        # Obtener el costo de producción
        costo = costo_produccion_producto(producto.id_producto)
        
        if costo is not None:
            # Calcular la rentabilidad (Precio - Costo de Producción)
            rentabilidad_producto = producto.precio - costo
            rentabilidad[producto.id_producto] = rentabilidad_producto
    
    # Encontrar el producto con la rentabilidad más alta
    producto_max_rentabilidad_id = max(rentabilidad, key=rentabilidad.get)
    
    # Obtener el producto con la mayor rentabilidad
    producto_max_rentabilidad = Productos.query.get(producto_max_rentabilidad_id)
    
    return producto_max_rentabilidad, rentabilidad[producto_max_rentabilidad_id]

        
    
        
            
            
             
        
        
        
    



    