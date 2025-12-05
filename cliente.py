import requests
import getpass
import os
# from requests.auth import HTTPBasicAuth
#from servidor import verificar_credenciales

servidor_url = "http://127.0.0.1:8000"
# servidor_url = "http://192.168.1.3:8000"


def ingresar_nombre_y_anio():
    nombre_movie = input(4*" " + "Ingrese nombre de la película: ")
    anio_movie = input(4*" " + "Ingrese año: ")
    return (nombre_movie, anio_movie)

def obtener_peliculas():
    respuesta = requests.get(f"{servidor_url}/peliculas")
    return (respuesta.json())


def obtener_pelicula():
    pelicula_titulo = input(4*" " + "Título de la película: ")
    respuesta = requests.get(f"{servidor_url}/peliculas/" + pelicula_titulo)
    return (respuesta.json())


def agregar_pelicula():
    titulo = input("Ingrese el título: ")
    año = int(input("Ingrese el año: "))
    elenco = []
    cond = input("Ingresar actor?[y/n]: ")
    if cond == "n":
        elenco = None
    else: 
        while cond == "y":
            actor = input("Ingrese nombre del actor: ")
            elenco.append(actor)
            cond = input("Ingresar otro actor?[y/n]: ")
    generos = []
    cond1 = input("Ingresar un género?[y/n]: ")
    if cond1 == "n":
        generos = None
    else: 
        while cond1 == "y":
            genero = input("Ingrese un género: ")
            generos.append(genero)
            cond1 = input("Ingresar otro género?[y/n]: ")
    href = input ("Ingrese href: ")
    thumbnail = input ("Ingrese url de la miniatura: ")
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
    titulo = input("Ingrese el título de la película a borrar: ")
    respuesta = requests.delete(f"{servidor_url}/peliculas/", params = {"pelicula_titulo": titulo})
    return (respuesta.json())


def editar_pelicula(titulo: str, anio: str):
    # 1. Obtener la película actual
    resp = requests.get(f"{servidor_url}/peliculas/{titulo}/{anio}")

    if resp.status_code != 200:
        print(4*" " + "Película no encontrada.")
        return

    pelicula = resp.json()

    print("\n=== EDITAR PELÍCULA ===")
    print(f"Título actual: {pelicula['title']}")
    nuevo_titulo = input(4*" " + "Nuevo título (enter para mantener): ").strip()

    print(f"Año actual: {pelicula['year']}")
    nuevo_anio = input(4*" " + "Nuevo año (enter para mantener): ").strip()

    print(f"Géneros actuales: {', '.join(pelicula['genres'])}")
    nuevos_generos = input(4*" " + "Nuevos géneros separados por coma (enter para mantener): ").strip()

    print(f"Elenco actual: {', '.join(pelicula['cast'])}")
    nuevo_cast = input(4*" " + "Nombre Actor separado por coma (enter para mantener): ").strip()

    print(f"Href actual: {pelicula['href']}")
    nuevo_href = input(4*" " + "Nuevo href (enter para mantener): ").strip()

    # 2. Construir el payload SOLO con lo que cambia
    payload = {}

    if nuevo_titulo:
        payload["title"] = nuevo_titulo

    if nuevo_anio:
        payload["year"] = int(nuevo_anio)

    if nuevos_generos:
        payload["genres"] = [g.strip() for g in nuevos_generos.split(",")]

    if nuevo_cast:
        payload["cast"] = [c.strip() for c in nuevo_cast.split(",")]

    if nuevo_href:
        payload["href"] = nuevo_href

    # 3. Enviar actualización (solo campos modificados)
    if payload:
        r = requests.put(f"{servidor_url}/peliculas/{titulo}/{anio}", json=payload)

        if r.status_code == 200:
            print("\nPelícula actualizada correctamente.")
        else:
            print("\nError al actualizar:", r.text)
    else:
        print("\nNo se realizaron cambios.")

# -------------------------------------------------------------

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_inicial():
    limpiar_pantalla()
    # print(os.name)
    print()
    print(3*" " + "┌" + 55*"─" + "┐")
    print(3*" " + "│" + 3*" " + "MENU" + 34*" " + "\033[3m(invitado)\033[0m" + 4*" " + "│")
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
    intentos = 3
    while(intentos > 0):
        limpiar_pantalla()
        print()
        print(3*" " + "┌" + 55*"─" + "┐")
        print(3*" " + "│" + 3*" " + "ACCEDER" + 45*" " + "│")
        print(3*" " + "├" + 55*"─" + "┤")
        print(3*" " + "│" + 55*" " + "│")
        print(3*" " + "│" + 3*" " + "Ingresá tu Usuario y Contraseña" + 21*" " + "│")
        print(3*" " + "│" + 55*" " + "│")
        print(3*" " + "└" + 55*"─" + "┘")
        print()
        usuario_str = input(4*" " + "Usuario: ")
        pass_str = input(4*" " + "Contraseña: ")
        print()
        respuesta = requests.get(f"{servidor_url}/protegido", auth=(usuario_str, pass_str))
 
        if respuesta.status_code == 200:
            menu_ppal(usuario_str)
            # print(respuesta)
            return
            
        intentos -= 1
        print(4*" " + 42*"*")
        print(4*" " + "*** Usuario y/o Contraseña INCORRECTOS ***")
        print(4*" " + f"***   Quedan: {intentos} intento/s restante/s   ***")
        print(4*" " + 42*"*")
        print()
        os.system("pause")
    print(4*" " + '*** ERROR ***')


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
    print(3*" " + "│" + 3*" " + "3 - Editar datos de una película" + 20*" " + "│")
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
        nombre, anio = ingresar_nombre_y_anio()
        print(editar_pelicula(nombre, anio))
    elif opcion == "4":
        print(borrar_pelicula())
    elif opcion == "x" or "X":
        print(4*" " + "*** ERR: opción no programada (Pendiente...) ***")
        print()
    else:
        print(4*" " + "Opción no válida")


if __name__ =="__main__":
    menu_inicial()