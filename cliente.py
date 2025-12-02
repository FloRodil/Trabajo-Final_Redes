import requests

servidor_url = "http://127.0.0.1:8000"

def obtener_peliculas():
    respuesta = requests.get(f"{servidor_url}/peliculas")
    return (respuesta.json())

def obtener_pelicula():
    pelicula_titulo = input("Título de la película: ")
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

    

def menu():
    print("Opción 1: Obtener datos de todas las películas")
    print("Opción 2: Obtener datos de una película por su título")
    print("Opción 3: Agregar datos de una película")
    print("Opción 4: Borrar una película")

    opcion = input("Ingrese el número de la opción seleccionada: ")

    if opcion == "1":
        print(obtener_peliculas())
    elif opcion == "2":
        print(obtener_pelicula())
    elif opcion == "3":
        print(agregar_pelicula())
    elif opcion == "4":
        print(borrar_pelicula())
    else:
        print("Opción no válida")

if __name__ =="__main__":
    menu()