#Para lograr esta validación de datos he usado la función isinstance()
#Validación de datos

def validar_datos(edades):
    for i in edades:
        if isinstance(i,int) and i >= 0:
            print(i)
        
edades = [23, -5, "20", 30, None, 15]
print("Salida:")
validar_datos(edades)

#Trabajando con try y except


#imprimir solamente los datos que se pueden convertir en enteros
def conv_enteros(datos):
    enteros = []
    for valor in datos:
        try:
            numero = int(valor)
            enteros.append(numero)
        except:
            pass
    return enteros
datos = [10, "20", "abc", None, 5.5, "30"]
print(conv_enteros(datos))


elementos = [10, "20", "abc", None, -5, 3.7, "15"]

def validar_datos(elementos):
    val_enteros = []
    
    for valor in elementos:
        try:
            numero = int(valor)
            if numero >=0:
                val_enteros.append(numero)
        except:
            pass
    return val_enteros

print(validar_datos(elementos))



#Ahora trabajaremos con diccionarios complejos
usuarios = [
    {"nombre":"Ana","edad":23},
    {"nombre": "Luis", "edad": 17},
    {"nombre": "Carlos", "edad": 30},
    {"nombre": "María", "edad": 15}
]

def mayor_edad(usuarios):
    mayores = []
    for valores in usuarios:
        if valores["edad"] >= 18:
            mayores.append(valores)
    return mayores

print(mayor_edad(usuarios))



#Ahora trabajamos con diccionarios sucios
d_usuarios = [
   {"nombre":"Ana","Edad":23},
   {"nombre":"Luis"},
   {"nombre":"Carlos","Edad":None},
   {"nombre":"Maria","Edad":15},
   {"edad":40} 
]


def usuario_completo(d_usuarios):
    
    usario_verificado = []
    for valor in d_usuarios:
        nombre = valor.get('nombre')
        edad = valor.get('Edad')
        
        if nombre is None or not isinstance(edad,int):
            continue
        
        if edad >=18:
            usario_verificado.append(valor)
    return usario_verificado
    
print(usuario_completo(d_usuarios))


#Devolver el promedio de edades validas
datos =  [
    {"nombre": "Denilson", "edad": 26},
    {"nombre": "Zamir", "edad": 24},
    {"nombre": "Sebastian", "edad": 21},
    {"nombre": "Diego", "edad": 21},
    {"nombre": "Dayana", "edad": 23},
    {"nombre": "Renzo", "edad": 22},
    {"nombre": "Kiara"},
    {"nombre": "Kelly", "edad":None},
    {"edad":40}
]


def validar_datos(datos):
    edad_validas = []
    for valores in datos:
        
        nombre = valores.get("nombre")
        edad = valores.get("edad")
        
        if nombre is None or not isinstance(edad,int):
            continue
        
        if edad >= 0:
            edad_validas.append(valores)
    
    return edad_validas
    
def promedio_edad(edades):
    promedio = 0
    suma = 0
    for valor in edades:
        edad = valor.get("edad")
        suma  = suma + edad
    
    promedio = suma/len(edades)
    
    return promedio
print(validar_datos(datos))
print(promedio_edad(validar_datos(datos)))

#Iterando diccionarios
datos =  [
    {"nombre": "Denilson", "edad": 15},
    {"nombre": "Zamir", "edad": 24},
    {"nombre": "Sebastian", "edad": 21},
    {"nombre": "Diego", "edad": 21},
    {"nombre": "Dayana", "edad": 12},
    {"nombre": "Renzo", "edad": 14},
    {"nombre": "Kiara"},
    {"nombre": "Kelly", "edad":None},
    {"edad":40}
]


def crear_usuario(datos):
    nombre = datos.get("nombre")
    edad = datos.get("edad")
    
    #validaciones
    if not isinstance(nombre,str) or not isinstance(edad,int):
        return None
    
    if edad < 0:
        return None
    
    return {
        "nombre":nombre,
        "edad": edad
    }
    

for persona in datos:
    usuarios = crear_usuario(persona)
    print(usuarios)
    
    

#Funcion registrar producto
productos = [
    {"nombre": "Laptop", "precio": 3500.50, "stock": 5},
    {"nombre": "Mouse", "precio": 45.90, "stock": 30},
    {"nombre": "Teclado", "precio": 120.00, "stock": 20},
    # Datos “sucios”
    {"nombre": "Monitor", "precio": None, "stock": 8},          # precio faltante
    {"nombre": "Audífonos", "precio": 95.50, "stock": None},    # stock faltante
    {"nombre": None, "precio": 35.00, "stock": 50},             # nombre faltante
    {"precio": 420.99, "stock": 10},                             # sin nombre
    {"nombre": "Impresora", "stock": 3},                          # sin precio
    {"nombre": "Webcam", "precio": 150.75},                       # sin stock
    {"nombre": "Parlantes", "precio": -80.00, "stock": 4},       # precio inválido (negativo)
    {"nombre": "Tablet", "precio": 900.00, "stock": -2},         # stock inválido (negativo)
    {"nombre": "Cargador", "precio": "25", "stock": 40},         # precio mal tipeado (string)
    {"nombre": 123, "precio": 15.00, "stock": 10},               # nombre mal tipeado (int)
]


def registrar_producto(productos):
    nombre = productos.get("nombre")
    precio = productos.get("precio")
    stock = productos.get("stock")
    
    #validaciones
    if not isinstance(nombre,str) or not isinstance(precio,float) or not isinstance(stock,int):
        return None
    
    if precio < 0 or stock < 0:
        return None
    
    return {
        "nombre":nombre,
        "precio": precio,
        "stock" : stock
    }
    

for pro in productos:
    elementos = registrar_producto(pro)
    print(elementos)
    
#Promedio de edad validadas
usuarios = [
    {"nombre": "Denilson", "edad": 15},
    {"nombre": "Zamir", "edad": 24},
    {"nombre": "Sebastian", "edad": 21},
    {"nombre": "Diego", "edad": 21},

    # Datos sucios
    {"nombre": "Dayana", "edad": None},        # edad faltante
    {"nombre": None, "edad": 18},              # nombre faltante
    {"edad": 30},                              # sin nombre
    {"nombre": "Renzo"},                       # sin edad
    {"nombre": "Kiara", "edad": -5},           # edad inválida (negativa)
    {"nombre": "Kelly", "edad": "20"},         # edad mal tipeada (string)
    {"nombre": 123, "edad": 22},               # nombre mal tipeado (int)
    {"nombre": "Luis", "edad": 15.5},          # edad mal tipeada (float)
    {"nombre": "", "edad": 19},                # nombre vacío
    {"nombre": "Ana", "edad": 0},              # borde: edad 0 (según tu lógica puede ser inválido)
]


def validar_usuarios(usuarios):
    usuarios_validos = []
    for valor in usuarios:
        nombre = valor.get("nombre")
        edad = valor.get("edad")
        
        if not isinstance(nombre,str) or not isinstance(edad,int):
            continue
        if edad > 0:
            usuarios_validos.append(valor)
    return usuarios_validos
    

def promedio_edad(edades):
    suma = 0
    promedio = 0 
    for valor in edades: 
        edad = valor.get("edad")
        suma = suma + edad
    
    promedio = suma/len(edades)
    
    return promedio

print(validar_usuarios(usuarios))
print("El promedio de la edad:")
print(promedio_edad(validar_usuarios(usuarios)))


#Productos - Simulación de una API
productos = [
    # Datos correctos
    {"producto": "Laptop", "cantidad": 5, "precio_unitario": 3500.50},
    {"producto": "Mouse", "cantidad": 20, "precio_unitario": 45.90},
    {"producto": "Teclado", "cantidad": 10, "precio_unitario": 120.00},

    # Datos sucios
    {"producto": "Monitor", "cantidad": None, "precio_unitario": 800.00},     # cantidad faltante
    {"producto": "Impresora", "cantidad": 3, "precio_unitario": None},        # precio faltante
    {"producto": None, "cantidad": 7, "precio_unitario": 150.00},             # producto faltante
    {"cantidad": 4, "precio_unitario": 60.00},                                # sin producto
    {"producto": "Webcam", "precio_unitario": 90.00},                         # sin cantidad
    {"producto": "Parlantes", "cantidad": 5},                                 # sin precio
    {"producto": "Tablet", "cantidad": -2, "precio_unitario": 900.00},        # cantidad inválida (negativa)
    {"producto": "USB", "cantidad": 10, "precio_unitario": -15.00},           # precio inválido (negativo)
    {"producto": "Cargador", "cantidad": "5", "precio_unitario": 25.00},      # cantidad mal tipeada (string)
    {"producto": "Funda", "cantidad": 3, "precio_unitario": "30"},            # precio mal tipeado (string)
    {"producto": 123, "cantidad": 2, "precio_unitario": 50.00},               # producto mal tipeado (int)
    {"producto": "", "cantidad": 1, "precio_unitario": 10.00},                # producto vacío
]

def registrar_pedido_api(productos):
    
    try:
        producto = productos["producto"]
        cantidad = int(productos["cantidad"])
        precio = float(productos["precio_unitario"])
    except(KeyError,TypeError,ValueError):
        return{
            "status":"error",
            "message":"Datos inválidos"
        }
        
    if not isinstance(producto,str) or producto.strip() == "":
        return{
            "status":"error",
            "message":"Producto inválido"
        }
    if cantidad <= 0 :
        return{
            "status": "error",
            "message": "Producto inválido"
        }
    if precio <= 0:
        return{
            "status": "error",
            "message": "producto inválido"
        }
    return{
        "status":"success",
        "productos":{
            "producto":producto,
            "cantidad": cantidad,
            "precio": precio,
            "total" : cantidad * precio
        }
    }
    

for producto in productos:
    print(registrar_pedido_api(producto))