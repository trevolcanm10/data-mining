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