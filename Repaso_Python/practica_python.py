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