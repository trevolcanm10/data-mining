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