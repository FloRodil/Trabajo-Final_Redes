import json #lo uso para manejar los json
import bcrypt #transforma string en hashes
import uvicorn
import secrets #1-12 se agregó
import os
from fastapi import FastAPI, HTTPException, Depends, status, Request #verificación de credenciales
# from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials #verificación de credenciales
from typing import Optional, Dict, Deque #1-12 se agregó Dict
from pydantic import BaseModel # valida, convierte y estructura datos JSON -> en objeto de la clase y el objeto en diccionario
from collections import deque
from datetime import datetime, timedelta

archivo_datos = "movies.json"
archivo_usuarios = "usuarios.json"

app = FastAPI()

# Cargar usuarios
def cargar_usuarios():
    with open("usuarios.json", "r", encoding="utf-8") as f:
        usuarios = json.load(f)

    # Convertir los hashes de str → bytes para bcrypt
    # Creamos un nuevo diccionario vacío
    usuarios_bytes = {}

    # Iteramos sobre cada par usuario-hash del diccionario original
    for u, h in usuarios.items():
    
    # Guardamos en el nuevo diccionario
        usuarios_bytes[u] = h.encode() # Convertimos el hash de string a bytes

    return usuarios_bytes

# Cargar datos
def cargar_datos():
    with open(archivo_datos, "r", encoding="utf-8") as a:
        print(len(json.load(a)))
        for clave, valor in json.load(a)[0]:
            print(f"{clave}: {type(valor).__name__}")
        #return json.load(a)


# Guardar datos    
def guardar_datos(datos):
    with open(archivo_datos, "w", encoding="utf-8") as a:
        json.dump(datos, a)


# Estructura de los datos de una película
class Pelicula(BaseModel):
    title: str
    year: int
    cast: Optional[list] = None
    genres: Optional[list] = None
    href: Optional[str] = None
    extract: Optional[str] = None
    thumbnail: Optional[str] = None
    # thumbnail_width: Optional[int] = 320
    # thumbnail_height: Optional[int] = 320

# -------Agregado 1-12 -------------------------------------------------------

# HTTPBasic() dependencia de Fastapli que detecta si 
# el request trae el encabezado HTTP Authorization: Basic <credenciales_base64>
# Decodifica ese Base64 y obtiene username y password

security = HTTPBasic() 

USUARIOS = cargar_usuarios()

# Autentificación de usuarios

def verificar_credenciales(credenciales: HTTPBasicCredentials = Depends(security)) -> str: #Depends(security), llama a HTTPBasic() y pasa credenciales a la función
    pwd_hash = USUARIOS.get(credenciales.username)
    if not pwd_hash or not bcrypt.checkpw(credenciales.password.encode(), pwd_hash): # bcrypt.checkpw() compara la contraseña ingresada (bytes) con el hash almacenado (bytes)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credenciales.username  # Devuelve el nombre del usuario autenticado

# #-------------------------------------------------------------------------------
# #Limitador

VENTANA = timedelta(seconds=1)   # Ventana de tiempo
MAX_PETICIONES = 10             # Máximo de peticiones dentro de la ventana

cubos_ip: Dict[str, Deque[datetime]] = {} #diccionario ip_cliente: cola con timestamps de sus peticiones

@app.middleware("http")
async def limitador(request: Request, call_next):
    ip = request.client.host #ip_cliente
    ahora = datetime.utcnow() #timestamp actual

    cubo = cubos_ip.setdefault(ip, deque()) #si la ip existe devuelve su cola sino crea una vacía

    # Eliminar timestamps fuera de la ventana
    while cubo and (ahora - cubo[0]) > VENTANA:
        cubo.popleft()

    # Verificar si se excedió el límite de peticiones
    if len(cubo) >= MAX_PETICIONES:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiadas solicitudes: límite 10 req/s",
        )

    cubo.append(ahora) #registra la peticion actual
    respuesta = await call_next(request) #continua el proceso
    return respuesta


@app.get("/protegido")
def protegido(usuario: str = Depends(verificar_credenciales)):
    return
    # return {"msg": f"Hola {usuario}, acceso permitido"}

#---------------------------------------------------------------------------


# Obtener todas las películas
@app.get("/peliculas")
def mostrar_peliculas():
    return cargar_datos()


# Obtener una película por su título
@app.get("/peliculas/{pelicula_titulo}")
def mostrar_pelicula(pelicula_titulo: str):
    datos = cargar_datos()
    coincidencias = []

    for pelicula in datos:
        if pelicula["title"].lower() == pelicula_titulo.lower():
            margen = 6*" "
            no_disp = "\033[3mNo disponible\033[0m"

            texto = (
                4* " " + f"{'-'*55}\n"
                + margen + f"Título: {pelicula['title']}\n"
                + margen + f"Año: {pelicula['year']}\n"
                + margen + f"Géneros: {', '.join(pelicula['genres']) if pelicula['genres'] else no_disp}\n"
                + margen + f"Elenco: {', '.join(pelicula['cast']) if pelicula['cast'] else no_disp}\n"
                + margen + f"Href: {pelicula['href']  if pelicula['href'] else no_disp}\n"
                # + 4* " " + f"{'-'*55}\n"
            )

            coincidencias.append(texto)

    if coincidencias:
        return "\n".join(coincidencias)

    raise HTTPException(status_code=404, detail="No encontrado")


# Obtener una película por su título y año  
@app.get("/peliculas/{titulo}/{anio}")
def obtener_pelicula(titulo: str, anio: int):
    datos = cargar_datos()

    for pelicula in datos:
        if pelicula["title"].lower() == titulo.lower() and pelicula["year"] == anio:
            return pelicula

    raise HTTPException(status_code=404, detail="Película no encontrada")


# Agregar una nueva película
@app.post("/peliculas")
#def agregar_pelicula(pelicula: Pelicula, usuario: str = Depends(verificar_credenciales)):
def agregar_pelicula(pelicula: Pelicula):
    datos = cargar_datos()
    datos.append(pelicula.model_dump()) # el método model.dump() es necesario para transformar el objeto película en un diccionario
    guardar_datos(datos)
    return{"mensaje": "Película agregada", "Película": pelicula}


# Borrar película por título
@app.delete("/peliculas")
#def borrar_pelicula(pelicula_titulo: str, usuario: str = Depends(verificar_credenciales)):
def borrar_pelicula(pelicula_titulo: str):
    datos = cargar_datos()
    for pelicula in datos:
        if pelicula["title"].lower() == pelicula_titulo.lower():
            print(pelicula["title"].lower())
            datos.remove(pelicula)
            guardar_datos(datos)
            return{"mensaje": "Película borrada", "Título": pelicula_titulo}


# Editar película por título y año
@app.put("/peliculas/{titulo}/{anio}")
def actualizar_pelicula(titulo: str, anio: int, cambios: Pelicula):
    datos = cargar_datos()

    for pelicula in datos:
        if pelicula["title"].lower() == titulo.lower() and pelicula["year"] == anio:

            # actualizar solo si llega un valor (no actualizar si es None)
            if cambios.title is not None and cambios.title != "":
                pelicula["title"] = cambios.title

            if cambios.year is not None:
                pelicula["year"] = cambios.year

            if cambios.genres is not None:
                pelicula["genres"] = cambios.genres

            if cambios.cast is not None:
                pelicula["cast"] = cambios.cast

            if cambios.href is not None and cambios.href != "":
                pelicula["href"] = cambios.href

            guardar_datos(datos)
            return {4*" " + "mensaje": "Película actualizada correctamente"}

    raise HTTPException(status_code=404, detail="Película no encontrada")




if __name__=="__main__":
    #cargar_datos()
    uvicorn.run("servidor:app", host="0.0.0.0", port=8000, reload=True)