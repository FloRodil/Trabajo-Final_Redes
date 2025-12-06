import requests
import os
# import getpass
# from requests.auth import HTTPBasicAuth
#from servidor import verificar_credenciales

servidor_url = "http://127.0.0.1:8000"
# servidor_url = "http://192.168.1.3:8000"

def existe_pelicula(titulo, anio):
    url = f"{servidor_url}/peliculas/{titulo}/{anio}"
    response = requests.get(url)
    return response.json()



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
    titulo = input(4*" " + "Ingresá el título: ")
    if titulo:
        anio = input(4*" " + "Ingresá el año: ")
        if anio:
            elenco_str = input(4*" " + "ingresar Nombre Actores separado por coma (enter para omitir): ").strip()
            generos_str = input(4*" " + "ingresar Géneros separados por coma (enter para omitir): ").strip()
            href = input(4*" " + "ingresar href (enter para omitir): ").strip()
            thumbnail = input (4*" " + "Ingrese url de la miniatura (enter para omitir): ").strip()

            elenco = [a.strip() for a in elenco_str.split(",")] if elenco_str else []
            generos = [g.strip() for g in generos_str.split(",")] if generos_str else []

            pelicula = {
                "title": titulo, 
                "year": anio, 
                "cast": elenco, 
                "genres": generos, 
                "href": href, 
                "thumbnail": thumbnail, 
                "thumbnail_width": 320, 
                "thumbnail_height": 320}
            
            respuesta = requests.post(f"{servidor_url}/peliculas/", json = pelicula)
            return (respuesta.json())
        
        else:
            print()
            return(4*" " + "*** El año es un campo obligatorio ***")
            # input("\nPresione ENTER para continuar...")
            
    else:
        print()
        return(4*" " + "*** El título es un campo obligatorio ***")
        # input("\nPresione ENTER para continuar...")
        
    
def borrar_pelicula(): #### Arreglar <<<
    titulo = input(4*" " + "Ingrese el título de la película a borrar: ")
    if titulo:
        anio_str = input(4*" " + "Ingrese el año de la película a borrar: ")
        if anio_str:
            print()
            print()
            anio = int(anio_str)
            #if existe_pelicula(titulo, anio):
            #print (existe_pelicula(titulo, anio))
            #cod_estado = existe_pelicula(titulo, anio).status_code
            #if cod_estado == 200:
            if existe_pelicula(titulo, anio) != False:
                respuesta = input(4*" " + f"¿¿¿ Estás seguro de borrar: {titulo} del año: {anio} ??? - [s/n]: ")
                if respuesta.lower() == "s": 
                    # respuesta = requests.delete(f"{servidor_url}/peliculas/", params = {"pelicula_titulo": titulo})
                    respuesta = requests.delete(f"{servidor_url}/peliculas/", params = {"pelicula_titulo": titulo, "pelicula_anio": anio})
                    # print("Status:", respuesta.status_code)
                    # print("Texto:", respuesta.text)
                    return (respuesta.json())
                else:
                    print()
                    return(4*" " + f"*** La película {titulo} del año {anio} NO FUE BORRADA ***")
            return(4*" " + f"La película {titulo} del año {anio}, NO existe en el JSON...")
        
        return(f"    El año es obligatorio.")
    return(f"    El nombre es obligatorio.")

def editar_pelicula(titulo: str, anio: int): # Funciona OK

    pelicula = existe_pelicula(titulo,anio)
    if pelicula == False:
        print(4*" " + "Película no encontrada.")
        return

    print(4*" " + "\n=== EDITAR PELÍCULA ===")
    
    print(4*" " + f"Título actual: {pelicula['title']}")
    nuevo_titulo = input(4*" " + "Nuevo título (enter para mantener): ").strip()

    print(4*" " + f"Año registrado: {pelicula['year']}")
    nuevo_anio = input(4*" " + "Nuevo año (enter para mantener): ").strip()

    print(4*" " + f"Géneros actuales: {', '.join(pelicula['genres']) if isinstance(pelicula.get('genres'), list) else 'sin datos'}")
    nuevos_generos = input(4*" " + "Nuevos géneros separados por coma (enter para mantener): ").strip()

    print(4*" " + f"Elenco actual: {', '.join(pelicula['cast']) if isinstance(pelicula.get('cast'), list) else 'sin datos'}")
    nuevo_cast = input(4*" " + "Nombre Actor separado por coma (enter para mantener): ").strip()

    print(4*" " + f"Href actual: {pelicula['href']}")
    nuevo_href = input(4*" " + "Nuevo href (enter para mantener): ").strip()

    # Se agrega sólo lo que se cambió con el input
    if nuevo_titulo:
        pelicula["title"] = nuevo_titulo

    if nuevo_anio:
        pelicula["year"] = int(nuevo_anio)

    if nuevos_generos:
        pelicula["genres"] = [g.strip() for g in nuevos_generos.split(",")]

    if nuevo_cast:
        pelicula["cast"] = [c.strip() for c in nuevo_cast.split(",")]

    if nuevo_href:
        pelicula["href"] = nuevo_href

    # Campos fijos:
    pelicula["thumbnail_width"] = 320
    pelicula["thumbnail_height"] = 320

    r = requests.put(f"{servidor_url}/peliculas/{titulo}/{anio}", json=pelicula)

    if r.status_code == 200:
        print(4*" " + "Película actualizada correctamente.")
    else:
        print(4*" " + "Error al actualizar:", r.text)


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
    print(3*" " + "│" + 3*" " + "X - Salir" + 43*" " + "│")
    print(3*" " + "│" + 55*" " + "│")
    print(3*" " + "└" + 55*"─" + "┘")
    print()

    opcion = input(4*" " + "Ingrese el número de la opción seleccionada: ")
    if opcion == "1":
        print(obtener_peliculas())

    elif opcion == "2":
        acceder()

    elif opcion == "?":
        return ""

    elif opcion.lower() == "x":
        print("\n    Saliendo de la api...")
        exit()
    
    else:
        print()
        print(4*" " + "*** Opción no válida ***")
        input("\nPresione ENTER para continuar...")
        menu_inicial()


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

    while True:  # ← bucle principal del menú

        limpiar_pantalla()
        print()
        print(3*" " + "┌" + 55*"─" + "┐")
        print(3*" " + "│" + 5*" " + "MENU" + (30-len(n_usuario))*" " 
              + "bienvenid@: " + "\033[33m" + n_usuario + "\033[0m" + 4*" " + "│")
        print(3*" " + "├" + 55*"─" + "┤")
        print(3*" " + "│" + 55*" " + "│")
        print(3*" " + "│" + 3*" " + "1 - Obtener datos de todas las películas" + 12*" " + "│")
        print(3*" " + "│" + 3*" " + "2 - Obtener datos de una película por su título" + 5*" " + "│")
        print(3*" " + "│" + 3*" " + "3 - Agregar película" + 32*" " + "│")
        print(3*" " + "│" + 3*" " + "4 - Editar datos de una película" + 20*" " + "│")
        print(3*" " + "│" + 3*" " + "5 - Borrar una película" + 29*" " + "│")
        print(3*" " + "│" + 55*" " + "│")
        print(3*" " + "│" + 3*" " + "6 - Log-Out" + 41*" " + "│")
        print(3*" " + "│" + 3*" " + "X - Salir" + 43*" " + "│")
        print(3*" " + "│" + 55*" " + "│")
        print(3*" " + "└" + 55*"─" + "┘")
        print()

        opcion = input(4*" " + "Ingrese el número de la opción seleccionada: ").strip()
        print()

        if opcion == "1":
            print(obtener_peliculas())
            input("\nPresione ENTER para continuar...")

        elif opcion == "2":
            print(obtener_pelicula())
            input("\nPresione ENTER para continuar...")

        elif opcion == "3":
            print(agregar_pelicula())
            input("\nPresione ENTER para continuar...")

        elif opcion == "4":
            nombre, anio = ingresar_nombre_y_anio()
            editar_pelicula(nombre, anio)
            input("\nPresione ENTER para continuar...")

        elif opcion == "5":
            print(borrar_pelicula())
            input("\nPresione ENTER para continuar...")

        elif opcion == "6":
            menu_inicial()
            input("\nPresione ENTER para continuar...")

        elif opcion.lower() == "x":
            print("\n    Saliendo de la api...")
            break  # ← rompe el bucle y sale del menú

        else:
            print(4*" " + "Opción no válida")
            input("\nPresione ENTER para continuar...")



if __name__ =="__main__":
    menu_inicial()