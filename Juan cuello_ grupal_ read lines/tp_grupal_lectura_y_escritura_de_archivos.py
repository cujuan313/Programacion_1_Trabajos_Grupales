##Paso 1 Funciones de validación de datos por teclado

def pedir_texto_solo_letras(mensaje):
    """
    Valida que el nombre o apellido contenga ÚNICAMENTE letras.
    """
    texto = input(mensaje).strip()
    while not texto.replace(" ", "").isalpha() or texto == "":
        print("Error: Ingrese únicamente letras (no se permiten números ni caracteres especiales).")
        texto = input(mensaje).strip()
    return texto.capitalize()


def pedir_legajo_valido():
    """
    Valida que el legajo sea de EXACTAMENTE 5 dígitos numéricos.
    """
    legajo = input("Ingrese legajo (5 dígitos): ").strip()
    while not legajo.isdigit() or len(legajo) != 5:
        print("Error: El legajo debe ser un número entero de EXACTAMENTE 5 dígitos.")
        legajo = input("Ingrese legajo (5 dígitos): ").strip()
    return legajo


def pedir_nota_valida():
    """
    Valida que la nota sea numérica y esté comprendida entre 1 y 10.
    """
    entrada = input("Ingrese nota promedio (1 a 10): ").strip()
    es_valido = False
    
    while not es_valido:
        if entrada.replace('.', '', 1).isdigit():
            nota = float(entrada)
            if 1 <= nota <= 10:
                es_valido = True
            else:
                print("Error: La nota debe estar comprendida dentro del rango entre 1 y 10.")
                entrada = input("Ingrese nota promedio (1 a 10): ").strip()
        else:
            print("Error: Debe ingresar un número válido para la nota (no se permiten letras).")
            entrada = input("Ingrese nota promedio (1 a 10): ").strip()
            
    return nota

### Paso 2 Validación de legajos existentes


def validar_existe_alumno(legajo, diccionario_alumnos):
    """
    Devuelve True si el legajo ya existe en el diccionario, False si no.
    """
    return legajo in diccionario_alumnos


### Paso 3 Leer el archivo alumnos.txt y cargar estructuras


def leer_alumnos(nombre_archivo="alumnos.txt"):
    lista_alumnos = []
    diccionario_alumnos = {}

    try:
        # 'a+' crea el archivo si no existe y permite lectura
        with open(nombre_archivo, "a+", encoding="utf-8") as archivo:
            archivo.seek(0)  # Movemos el puntero al inicio
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
        print(f"Error al intentar leer o crear el archivo '{nombre_archivo}': {e}")

    return lista_alumnos, diccionario_alumnos


### Paso 4  Agregar un alumno

def agregar_alumno(lista_alumnos, diccionario_alumnos, nombre_archivo="alumnos.txt"):
    print("\n--- AGREGAR NUEVO ALUMNO ---")
    legajo = pedir_legajo_valido()

    # Validar si el legajo existe
    if validar_existe_alumno(legajo, diccionario_alumnos):
        print(f"El legajo {legajo} ya existe en el archivo alumnos.txt, no se permite su escritura")
        return

    nombre = pedir_texto_solo_letras("Ingrese nombre: ")
    apellido = pedir_texto_solo_letras("Ingrese apellido: ")
    nota = pedir_nota_valida()

    nota_str = str(int(nota)) if nota.is_integer() else str(nota)
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

        print(f"¡El alumno {nombre} {apellido} fue guardado exitosamente!")

    except IOError as e:
        print(f"Error de escritura al guardar en '{nombre_archivo}': {e}")


### Paso 5 Filtrar y guardar alumnos aprobados

def guardar_aprobados(lista_alumnos, archivo_salida="aprobados.txt"):
    print("\n--- GENERANDO ARCHIVO DE APROBADOS ---")
    aprobados = [alum for alum in lista_alumnos if alum["nota"] >= 6]

    try:
        # Generar archivo de aprobados
        with open(archivo_salida, "w", encoding="utf-8") as archivo:
            for alum in aprobados:
                nota_str = str(int(alum["nota"])) if alum["nota"].is_integer() else str(alum["nota"])
                linea = f"{alum['nombre']}; {alum['apellido']};{alum['legajo']};{nota_str}\n"
                archivo.write(linea)

        print(f"Archivo '{archivo_salida}' generado con éxito ({len(aprobados)} aprobados).")

        # Mostrar por pantalla el contenido
        print(f"\n--- CONTENIDO DE {archivo_salida.upper()} ---")
        with open(archivo_salida, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if contenido:
                print(contenido)
            else:
                print("No se encontraron alumnos aprobados.")

    except IOError as e:
        print(f"Error de lectura/escritura al procesar '{archivo_salida}': {e}")


### Paso 6 Menú interactivo y ejecución


def menu():
    # Inicialización: Lee alumnos.txt y carga las estructuras
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
            print("Saliendo del sistema...")

        else:
            print("Opción inválida. Intente de nuevo.")

# Para ejecutar el programa completo:
menu()
