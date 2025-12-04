import requests
import os

servidor_url = "http://127.0.0.1:8000"
# servidor_url = "http://192.168.1.3:8000"

def obtener_peliculas():
    respuesta = requests.get(f"{servidor_url}/peliculas")
    return (respuesta.json())

def obtener_pelicula():
    pelicula_titulo = input(4*" " + "Título de la película: ")
    respuesta = requests.get(f"{servidor_url}/peliculas/" + pelicula_titulo)
    return (respuesta.json())

def agregar_pelicula():
    titulo = input(4*" " + "Ingrese el título: ")
    año = int(input(4*" " + "Ingrese el año: "))
    elenco = []
    cond = input(4*" " + "Ingresar actor?[y/n]: ")
    if cond == "n":
        elenco = None
    else: 
        while cond == "y":
            actor = input(4*" " + "Ingrese nombre del actor: ")
            elenco.append(actor)
            cond = input(4*" " + "Ingresar otro actor?[y/n]: ")
    generos = []
    cond1 = input(4*" " + "Ingresar un género?[y/n]: ")
    if cond1 == "n":
        generos = None
    else: 
        while cond1 == "y":
            genero = input(4*" " + "Ingrese un género: ")
            generos.append(genero)
            cond1 = input(4*" " + "Ingresar otro género?[y/n]: ")
    href = input ("Ingrese href: ")
    thumbnail = input (4*" " + "Ingrese url de la miniatura: ")
    # ancho =  input ("Ingrese ancho de la miniatura: ")
    # if ancho:
    #     thumbnail_width = int(ancho)
    # else:
    #     thumbnail_width = None
    # alto = input ("Ingrese ancho de la miniatura: ")
    # if alto:
    #     thumbnail_height = int(alto)
    # else:
    #     thumbnail_height = None
    pelicula = {
        "title": titulo, 
        "year": año, 
        "cast": elenco, 
        "genres": generos, 
        "href": href, 
        "thumbnail": thumbnail, 
        "thumbnail_width": 320, 
        "thumbnail_height": 320}
    respuesta = requests.post(f"{servidor_url}/peliculas/", json = pelicula)
    return (respuesta.json())

def borrar_pelicula():
    titulo = input(4*" " + "Ingrese el título de la película a borrar: ")
    respuesta = requests.delete(f"{servidor_url}/peliculas/", params = {"pelicula_titulo": titulo})
    return (respuesta.json())
    
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

nombre_usuario = "invitado"

def menu_inicial():
    limpiar_pantalla()
    # print(os.name)
    print()
    print(3*" " + "┌" + 55*"─" + "┐")
    # print(3*" " + "│" + 5*" " + "MENU" + (29-len(nombre_usuario))*" " + "hola: (" + nombre_usuario + ")" + 4*" " + "│")
    print(3*" " + "│" + 5*" " + "MENU" + 32*" " + "(invitado)" + 4*" " + "│")
    print(3*" " + "├" + 55*"─" + "┤")
    print(3*" " + "│" + 55*" " + "│")
    print(3*" " + "│" + 3*" " + "1 - Obtener datos de todas las películas" + 12*" " + "│")
    print(3*" " + "│" + 3*" " + "2 - Acceder (log-in)" + 32*" " + "│")
    print(3*" " + "│" + 55*" " + "│")
    print(3*" " + "│" + 3*" " + "? - Ayuda" + 43*" " + "│")
    print(3*" " + "│" + 55*" " + "│")
    print(3*" " + "└" + 55*"─" + "┘")
    print()

    opcion = input(4*" " + "Ingrese el número de la opción seleccionada: ")

    if opcion == "1":
        print(obtener_peliculas())
    elif opcion == "2":
        acceder()
    else:
        print(4*" " + "Opción no válida")


def acceder():
    limpiar_pantalla()
    print()
    print(3*" " + "┌" + 55*"─" + "┐")
    print(3*" " + "│" + 5*" " + "ACCEDER" + 43*" " + "│")
    print(3*" " + "├" + 55*"─" + "┤")
    print(3*" " + "│" + 55*" " + "│")
    print(3*" " + "│" + 3*" " + "Ingresá tu usuario y contraseña" + 21*" " + "│")
    print(3*" " + "│" + 55*" " + "│")
    print(3*" " + "└" + 55*"─" + "┘")
    print()
    usuario_str = input(4*" " + "Usuario: ")
    # pass_str = input(4*" " + "Contraseña: ")

    if True: #cambiar por la función de validación
        menu_ppal(usuario_str)
    else:
        prin("error")


def menu_ppal(n_usuario):
    limpiar_pantalla()
    # print(os.name)
    print()
    print(3*" " + "┌" + 55*"─" + "┐")
    print(3*" " + "│" + 5*" " + "MENU" + (30-len(n_usuario))*" " + "bienvenid@: " + "\033[33m" + n_usuario + "\033[0m" + 4*" " + "│")
    print(3*" " + "├" + 55*"─" + "┤")
    print(3*" " + "│" + 55*" " + "│")
    print(3*" " + "│" + 3*" " + "1 - Obtener datos de todas las películas" + 12*" " + "│")
    print(3*" " + "│" + 3*" " + "2 - Obtener datos de una película por su título" + 5*" " + "│")
    print(3*" " + "│" + 3*" " + "3 - Agregar datos de una película" + 19*" " + "│")
    print(3*" " + "│" + 3*" " + "4 - Borrar una película" + 29*" " + "│")
    print(3*" " + "│" + 55*" " + "│")
    print(3*" " + "│" + 3*" " + "X - Salir" + 43*" " + "│")
    print(3*" " + "│" + 55*" " + "│")
    print(3*" " + "└" + 55*"─" + "┘")
    print()

    opcion = input(4*" " + "Ingrese el número de la opción seleccionada: ")
    print()

    if opcion == "1":
        print(obtener_peliculas())
    elif opcion == "2":
        print(obtener_pelicula())
    elif opcion == "3":
        print(agregar_pelicula())
    elif opcion == "4":
        print(borrar_pelicula())
    elif opcion == "x" or "X":
        print(4*" " + "*** ERR: opción no programada (Pendiente...) ***")
        print()
    else:
        print(4*" " + "Opción no válida")

if __name__ =="__main__":
    menu_inicial()