

from os import system
from models.ingredientes import Ingredientes
from models.productos import Productos
from models.productosingredientes import Productosingredientes
from models import db




def validacion_sano(numero_calorias, es_vegetariano):
    if numero_calorias < 100 or es_vegetariano:
        return True
    else:
        return False
    

def abastecer(tipo_ingrediente, inventario):

    if tipo_ingrediente == "Base":
        inventario += 5
    else:
        inventario += 10
    return inventario


def conteo_calorias(self, numero_calorias):
    if not isinstance(numero_calorias, list): 
        raise ValueError("El parámetro 'numero_calorias' debe ser una lista de números.")
    
    conteo_calorias_producto = round(sum(numero_calorias) * 0.95, 2)
    
    return conteo_calorias_producto



def costo_produccion_producto(producto_id):
    producto = Productos.query.get(producto_id)
    
    if not producto:
        return None  
    
    costo_total = producto.precio
    
    ingredientes_relacionados = Productosingredientes.query.filter_by(id_producto=producto_id).all()
    
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

        


        
            
            
             
        
        
        
    



    