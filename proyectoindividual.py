
from datetime import datetime, date, timedelta

libros = []
usuarios = []
prestamos = []

multa_por_dia = 1000

def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()

        if texto != "":
            return texto
        else:
            print("Error: Este campo no puede quedar vacio.")


def leer_entero(mensaje, minimo=1):
    while True:
        try:
            numero = int(input(mensaje))

            if numero >= minimo:
                return numero
            else:
                print("Error: Ingresa un numero mayor o igual a", minimo)

        except ValueError:
            print("Error: Debes ingresar un numero entero.")


def buscar_libro(codigo):
    for libro in libros:
        if libro["codigo"] == codigo:
            return libro
    return None


def buscar_usuario(documento):
    for usuario in usuarios:
        if usuario["documento"] == documento:
            return usuario
    return None

def registrar_libro():
    print("REGISTRAR LIBRO")

    codigo = leer_texto("Codigo del libro: ")

    if buscar_libro(codigo) is not None:
        print("Error: Ya existe un libro con ese codigo.")
        return

    titulo = leer_texto("Titulo: ")
    autor = leer_texto("Autor: ")
    cantidad = leer_entero("Cantidad de ejemplares: ")

    nuevo_libro = {
        "codigo": codigo,
        "titulo": titulo,
        "autor": autor,
        "cantidad": cantidad,
        "disponibles": cantidad
    }

    libros.append(nuevo_libro)

    print("Libro registrado correctamente.")

def registrar_usuario():
    print("REGISTRAR USUARIO")

    documento = leer_texto("Documento del usuario: ")

    if buscar_usuario(documento) is not None:
        print("Error: Este usuario ya esta registrado.")
        return

    nombre = leer_texto("Nombre completo: ")
    telefono = leer_texto("Telefono: ")

    nuevo_usuario = {
        "documento": documento,
        "nombre": nombre,
        "telefono": telefono
    }

    usuarios.append(nuevo_usuario)

    print("Usuario registrado correctamente.")

def mostrar_libros():
    print("LISTADO DE LIBROS")

    if len(libros) == 0:
        print("Todavia no hay libros registrados.")
        return

    for libro in libros:
        print("-----------------------------")
        print("Codigo:", libro["codigo"])
        print("Titulo:", libro["titulo"])
        print("Autor:", libro["autor"])
        print("Cantidad:", libro["cantidad"])
        print("Disponibles:", libro["disponibles"])

def mostrar_usuarios():
    print("\n--- LISTADO DE USUARIOS ---")

    if len(usuarios) == 0:
        print("Todavia no hay usuarios registrados.")
        return

    for usuario in usuarios:
        print("-----------------------------")
        print("Documento:", usuario["documento"])
        print("Nombre:", usuario["nombre"])
        print("Telefono:", usuario["telefono"])

def prestar_libro():
    print("\n--- PRESTAR LIBRO ---")

    if len(libros) == 0 or len(usuarios) == 0:
        print("Primero debes registrar libros y usuarios.")
        return

    codigo = leer_texto("Codigo del libro: ")
    libro = buscar_libro(codigo)

    if libro is None:
        print("Error: El libro no existe.")
        return

    if libro["disponibles"] <= 0:
        print("No hay ejemplares disponibles de este libro.")
        return

    documento = leer_texto("Documento del usuario: ")
    usuario = buscar_usuario(documento)

    if usuario is None:
        print("Error: El usuario no esta registrado.")
        return

    dias = leer_entero("Dias del prestamo: ")

    fecha_prestamo = date.today()
    fecha_devolucion = fecha_prestamo + timedelta(days=dias)

    nuevo_prestamo = {
        "numero": len(prestamos) + 1,
        "codigo_libro": codigo,
        "documento_usuario": documento,
        "fecha_prestamo": fecha_prestamo,
        "fecha_devolucion": fecha_devolucion,
        "devuelto": False,
        "multa": 0
    }

    prestamos.append(nuevo_prestamo)
    libro["disponibles"] -= 1

    print("\nPrestamo realizado correctamente.")
    print("Numero de prestamo:", nuevo_prestamo["numero"])
    print("Usuario:", usuario["nombre"])
    print("Libro:", libro["titulo"])
    print("Fecha limite de devolucion:",
          fecha_devolucion.strftime("%d/%m/%Y"))


def mostrar_prestamos():
    print("LISTADO DE PRESTAMOS")

    if len(prestamos) == 0:
        print("No hay prestamos registrados.")
        return

    for prestamo in prestamos:

        libro = buscar_libro(prestamo["codigo_libro"])
        usuario = buscar_usuario(prestamo["documento_usuario"])

        print("-----------------------------")
        print("Numero:", prestamo["numero"])

        if libro is not None:
            print("Libro:", libro["titulo"])

        if usuario is not None:
            print("Usuario:", usuario["nombre"])

        print("Fecha de prestamo:",
              prestamo["fecha_prestamo"].strftime("%d/%m/%Y"))

        print("Fecha de devolucion:",
              prestamo["fecha_devolucion"].strftime("%d/%m/%Y"))

        if prestamo["devuelto"]:
            print("Estado: Devuelto")
            print("Multa pagada o pendiente:", prestamo["multa"])
        else:
            print("Estado: Prestado")

def devolver_libro():
    print("DEVOLVER LIBRO")

    activos = []

    for prestamo in prestamos:
        if not prestamo["devuelto"]:
            activos.append(prestamo)

    if len(activos) == 0:
        print("No hay prestamos pendientes de devolucion.")
        return

    print("\nPrestamos pendientes:")

    for prestamo in activos:
        print("Prestamo:", prestamo["numero"],
              "| Codigo del libro:", prestamo["codigo_libro"])

    numero = leer_entero("Numero del prestamo que deseas devolver: ")

    encontrado = None

    for prestamo in prestamos:
        if prestamo["numero"] == numero and not prestamo["devuelto"]:
            encontrado = prestamo
            break

    if encontrado is None:
        print("Error: No existe ese prestamo pendiente.")
        return

    fecha_actual = date.today()

    retraso = (fecha_actual - encontrado["fecha_devolucion"]).days

    if retraso > 0:
        multa = retraso * multa_por_dia
    else:
        multa = 0

    encontrado["devuelto"] = True
    encontrado["multa"] = multa

    libro = buscar_libro(encontrado["codigo_libro"])

    if libro is not None:
        libro["disponibles"] += 1

    print("Devolucion realizada correctamente.")

    if retraso > 0:
        print("Dias de retraso:", retraso)
        print("Multa total: $", multa)
    else:
        print("El libro fue devuelto a tiempo.")
        print("No hay multas.")

    print("Gracias por utilizar la biblioteca.")


def consultar_multas():
    print("CONSULTA DE MULTAS")

    hay_multas = False
    total_multas = 0

    for prestamo in prestamos:

        if prestamo["devuelto"] and prestamo["multa"] > 0:

            usuario = buscar_usuario(prestamo["documento_usuario"])

            print("-----------------------------")
            print("Prestamo:", prestamo["numero"])

            if usuario is not None:
                print("Usuario:", usuario["nombre"])

            print("Multa: $", prestamo["multa"])

            total_multas += prestamo["multa"]
            hay_multas = True

    if not hay_multas:
        print("No hay multas registradas.")

    print("-----------------------------")
    print("Total de multas: $", total_multas)


def menu():

    while True:
        print("BIBLIOTECA DEL BARRIO")
        print("1. Registrar libro")
        print("2. Registrar usuario")
        print("3. Mostrar libros")
        print("4. Mostrar usuarios")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Mostrar prestamos")
        print("8. Consultar multas")
        print("9. Salir")


        try:
            opcion = int(input("Selecciona una opcion: "))

            if opcion == 1:
                registrar_libro()

            elif opcion == 2:
                registrar_usuario()

            elif opcion == 3:
                mostrar_libros()

            elif opcion == 4:
                mostrar_usuarios()

            elif opcion == 5:
                prestar_libro()

            elif opcion == 6:
                devolver_libro()

            elif opcion == 7:
                mostrar_prestamos()

            elif opcion == 8:
                consultar_multas()

            elif opcion == 9:
                print("Gracias por utilizar el sistema.")
                print("Programa finalizado.")
                break

            else:
                print("Opcion incorrecta. Selecciona del 1 al 9.")

        except ValueError:
            print("Error: Debes escribir un numero valido.")

        except Exception as error:
            print("Ocurrio un problema inesperado.")
            print("El programa seguira funcionando.")
            print("Detalle:", error)

menu()
