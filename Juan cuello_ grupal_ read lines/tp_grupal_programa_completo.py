# ==========================================
# FUNCIONES AUXILIARES DE VALIDACIÓN
# ==========================================

def pedir_texto_solo_letras(mensaje):
    """
    Pide un texto al usuario y valida que contenga ÚNICAMENTE letras y espacios.
    Si el usuario ingresa números o símbolos, muestra un error y lo vuelve a pedir.
    """
    texto = input(mensaje).strip()
    # .replace(' ', '') permite nombres o apellidos compuestos como "De La Cruz"
    while not texto.replace(" ", "").isalpha() or texto == "":
        print("Error: Debe ingresar únicamente letras (no se permiten números ni caracteres especiales).")
        texto = input(mensaje).strip()
    return texto.capitalize()


def pedir_legajo_valido():
    """
    Pide un legajo y valida que sea exactamente de 5 dígitos numéricos.
    Si el usuario ingresa letras o un número de diferente cantidad de dígitos, muestra un error.
    """
    legajo = input("Ingrese legajo (5 dígitos): ").strip()
    while not legajo.isdigit() or len(legajo) != 5:
        print("Error: El legajo debe ser un número entero de EXACTAMENTE 5 dígitos (ejemplo: 53365).")
        legajo = input("Ingrese legajo (5 dígitos): ").strip()
    return legajo


def pedir_nota_valida():
    """
    Pide la nota promedio y valida que sea numérica y esté comprendida entre 1 y 10.
    Si el usuario ingresa letras o un rango inválido, muestra un error.
    """
    entrada = input("Ingrese nota promedio (entre 1 y 10): ").strip()
    es_valido = False
    
    while not es_valido:
        # Verificamos si es número entero o flotante
        if entrada.replace('.', '', 1).isdigit():
            nota = float(entrada)
            if 1 <= nota <= 10:
                es_valido = True
            else:
                print("Error: La nota debe estar comprendida dentro del rango entre 1 y 10.")
                entrada = input("Ingrese nota promedio (entre 1 y 10): ").strip()
        else:
            print("Error: Debe ingresar un número válido para la nota (no se permiten letras).")
            entrada = input("Ingrese nota promedio (entre 1 y 10): ").strip()
            
    return nota


# ==========================================
# FUNCIONES OBLIGATORIAS DEL TRABAJO PRÁCTICO
# ==========================================

def validar_existe_alumno(legajo, diccionario_alumnos):
    """
    Valida si el número de legajo ya existe en el diccionario.
    Devuelve True si existe, False si no.
    """
    return legajo in diccionario_alumnos


def leer_alumnos(nombre_archivo="alumnos.txt"):
    """
    Lee el archivo alumnos.txt, crea el archivo vacío si no existe y devuelve:
    1. Una lista de listas/diccionarios con todos los alumnos.
    2. Un diccionario donde la clave es el LEGAJO del alumno.
    """
    lista_alumnos = []
    diccionario_alumnos = {}

    try:
        # Modo 'a+' crea el archivo si no existe y nos permite leerlo
        with open(nombre_archivo, "a+", encoding="utf-8") as archivo:
            archivo.seek(0) # Mover el puntero al inicio del archivo para leer
            for linea in archivo:
                linea_limpia = linea.strip()
                if linea_limpia:
                    datos = linea_limpia.split(";")
                    if len(datos) == 4:
                        nombre = datos[0].strip()
                        apellido = datos[1].strip()
                        legajo = datos[2].strip()
                        nota = float(datos[3].strip())

                        alumno = {
                            "nombre": nombre,
                            "apellido": apellido,
                            "legajo": legajo,
                            "nota": nota
                        }
                        lista_alumnos.append(alumno)
                        diccionario_alumnos[legajo] = alumno

    except IOError as e:
        print(f"Error de E/S al intentar acceder al archivo '{nombre_archivo}': {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado al procesar los datos: {e}")

    return lista_alumnos, diccionario_alumnos


def agregar_alumno(lista_alumnos, diccionario_alumnos, nombre_archivo="alumnos.txt"):
    """
    Solicita los datos del nuevo alumno validando cada campo.
    Verifica que el legajo no exista. Si es correcto, lo guarda en el archivo
    y actualiza tanto la lista como el diccionario en memoria.
    """
    print("\n--- AGREGAR NUEVO ALUMNO ---")
    legajo = pedir_legajo_valido()

    # Requisito: Validar si el legajo ya existe
    if validar_existe_alumno(legajo, diccionario_alumnos):
        print(f"El legajo {legajo} ya existe en el archivo alumnos.txt, no se permite su escritura")
        return

    nombre = pedir_texto_solo_letras("Ingrese nombre: ")
    apellido = pedir_texto_solo_letras("Ingrese apellido: ")
    nota = pedir_nota_valida()

    # Formateo de la nota: si es entera (ej: 8.0) la muestra como 8
    nota_str = str(int(nota)) if nota.is_integer() else str(nota)

    # Formato requerido: nombre; apellido; legajo; notapromedio
    linea_a_escribir = f"{nombre}; {apellido};{legajo};{nota_str}\n"

    try:
        with open(nombre_archivo, "a", encoding="utf-8") as archivo:
            archivo.write(linea_a_escribir)

        # Actualizamos las estructuras en memoria
        nuevo_alumno = {
            "nombre": nombre,
            "apellido": apellido,
            "legajo": legajo,
            "nota": nota
        }
        lista_alumnos.append(nuevo_alumno)
        diccionario_alumnos[legajo] = nuevo_alumno

        print(f"¡El alumno {nombre} {apellido} fue registrado e ingresado con éxito en el archivo!")

    except IOError as e:
        print(f"Error de lectura/escritura al intentar guardar en '{nombre_archivo}': {e}")


def guardar_aprobados(lista_alumnos, archivo_salida="aprobados.txt"):
    """
    Filtra a los alumnos aprobados (nota >= 6), genera el archivo aprobados.txt
    y muestra por pantalla el contenido guardado.
    """
    print("\n--- GENERANDO ARCHIVO DE APROBADOS ---")
    aprobados = [alum for alum in lista_alumnos if alum["nota"] >= 6]

    try:
        with open(archivo_salida, "w", encoding="utf-8") as archivo:
            for alum in aprobados:
                nota_str = str(int(alum["nota"])) if alum["nota"].is_integer() else str(alum["nota"])
                linea = f"{alum['nombre']}; {alum['apellido']};{alum['legajo']};{nota_str}\n"
                archivo.write(linea)

        print(f"Archivo '{archivo_salida}' generado correctamente con {len(aprobados)} alumno(s) aprobados.")

        # Mostrar por pantalla el contenido generado de aprobados.txt
        print(f"\n--- CONTENIDO DE {archivo_salida.upper()} ---")
        with open(archivo_salida, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if contenido:
                print(contenido)
            else:
                print("No hay alumnos aprobados registrados en el archivo.")

    except IOError as e:
        print(f"Error de escritura/lectura al procesar '{archivo_salida}': {e}")


# ==========================================
# MENÚ PRINCIPAL DEL PROGRAMA
# ==========================================

def menu():
    # Requisito técnico: Al iniciar se lee el archivo y se cargan los datos y el diccionario
    lista_alumnos, diccionario_alumnos = leer_alumnos("alumnos.txt")

    opcion = ""
    while opcion != "4":
        print("\n==========================================")
        print("    MENÚ DE GESTIÓN ACADÉMICA DE ALUMNOS  ")
        print("==========================================")
        print("1. Ver alumnos (contenido de alumnos.txt)")
        print("2. Agregar alumno")
        print("3. Generar y mostrar archivo de aprobados")
        print("4. Salir")

        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            print("\n--- CONTENIDO DE ALUMNOS.TXT ---")
            if not lista_alumnos:
                print("El archivo 'alumnos.txt' no contiene registros.")
            else:
                for alum in lista_alumnos:
                    print(f"Nombre: {alum['nombre']} {alum['apellido']} | Legajo: {alum['legajo']} | Nota Promedio: {alum['nota']}")

        elif opcion == "2":
            agregar_alumno(lista_alumnos, diccionario_alumnos, "alumnos.txt")

        elif opcion == "3":
            guardar_aprobados(lista_alumnos, "aprobados.txt")

        elif opcion == "4":
            print("Saliendo del programa...")

        else:
            print("Opción inválida. Por favor, seleccione una opción entre 1 y 4.")

# Ejecutar el programa
menu()