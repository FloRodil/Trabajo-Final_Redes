import json
import uvicorn
#import secrets
import bcrypt
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
from typing import Optional, Dict, Deque
from pydantic import BaseModel
from collections import deque
from datetime import datetime, timedelta

archivo_datos = "movies.json"
archivo_usuarios = "usuarios.json"
archivo_ayuda = "ayuda.json"

app = FastAPI()

# Cargar usuarios
def cargar_usuarios():
    with open("usuarios.json", "r", encoding="utf-8") as f:
        usuarios = json.load(f)

    usuarios_bytes = {}

    for u, h in usuarios.items():
        usuarios_bytes[u] = h.encode()
    return usuarios_bytes

# Cargar datos
def cargar_datos():
    with open(archivo_datos, "r", encoding="utf-8") as a:
        return json.load(a)

#Cargar ayuda
def cargar_ayuda():
    with open(archivo_ayuda, "r", encoding="utf-8") as a:
        return json.load(a)
    
# Guardar datos    
def guardar_datos(datos):
    with open(archivo_datos, "w", encoding="utf-8") as a:
        json.dump(datos, a)


# Estructura de los datos de una película
class Pelicula(BaseModel):
    title: str
    year: int
    cast: Optional[list] = []
    genres: Optional[list] = []
    href: Optional[str] = None
    extract: Optional[str] = None
    thumbnail: Optional[str] = None
    thumbnail_width: Optional[int] = 320
    thumbnail_height: Optional[int] = 320

security = HTTPBasic() 

USUARIOS = cargar_usuarios()


# Autentificación de usuarios
def verificar_credenciales(credenciales: HTTPBasicCredentials = Depends(security)) -> str: 
    pwd_hash = USUARIOS.get(credenciales.username)
    if not pwd_hash or not bcrypt.checkpw(credenciales.password.encode(), pwd_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credenciales.username

#Limitador
VENTANA = timedelta(seconds=1)   # Ventana de tiempo
MAX_PETICIONES = 10             # Máximo de peticiones dentro de la ventana

cubos_ip: Dict[str, Deque[datetime]] = {}

@app.middleware("http")
async def limitador(request: Request, call_next):
    ip = request.client.host 
    ahora = datetime.utcnow() 

    cubo = cubos_ip.setdefault(ip, deque())

    # Eliminar timestamps fuera de la ventana
    while cubo and (ahora - cubo[0]) > VENTANA:
        cubo.popleft()

    # Verificar si se excedió el límite de peticiones
    if len(cubo) >= MAX_PETICIONES:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiadas solicitudes: límite 10 req/s",
        )

    cubo.append(ahora)
    respuesta = await call_next(request)
    return respuesta


# Existe película por su título y año  
@app.get("/peliculas/{titulo}/{anio}")
def existe_pelicula(titulo: str, anio: int):
    datos = cargar_datos()

    for pelicula in datos:
        if pelicula["title"].lower() == titulo.lower() and pelicula["year"] == anio:
            return pelicula
    return False


@app.get("/protegido")
def protegido(usuario: str = Depends(verificar_credenciales)):
    return {"msg": f"Hola {usuario}, acceso permitido"}


# Obtener todas las películas
@app.get("/peliculas")
def mostrar_peliculas():
    return cargar_datos()


# Obtener ayuda
@app.get("/ayuda")
def mostrar_ayuda():
    return cargar_ayuda()


# Obtener una película por su título
@app.get("/peliculas/{pelicula_titulo}")
def mostrar_pelicula(pelicula_titulo: str, usuario: str = Depends(verificar_credenciales)):
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
            )

            coincidencias.append(texto)

    if coincidencias:
        return "\n".join(coincidencias)
    raise HTTPException(status_code=404, detail="Película no encontrada...")


# Obtener una película por su título y año  
@app.get("/peliculas/{titulo}/{anio}")
def obtener_pelicula(titulo: str, anio: int, usuario: str = Depends(verificar_credenciales)):
    datos = cargar_datos()

    for pelicula in datos:
        if pelicula["title"].lower() == titulo.lower() and pelicula["year"] == anio:
            return pelicula

    raise HTTPException(status_code=404, detail="Película no encontrada")


# Agregar una nueva película
@app.post("/peliculas")
def agregar_pelicula(pelicula: Pelicula, usuario: str = Depends(verificar_credenciales)):
    datos = cargar_datos()
    datos.append(pelicula.model_dump())
    guardar_datos(datos)
    return(f"\n    Película '{pelicula.title}' agregada EXITOSAMENTE.")


# Borrar película por título y año
@app.delete("/peliculas")
def borrar_pelicula(pelicula_titulo: str, pelicula_anio: int, usuario: str = Depends(verificar_credenciales)):
    datos = cargar_datos()
    for pelicula in datos:
        if pelicula["title"].lower() == pelicula_titulo.lower() and pelicula["year"] == pelicula_anio:
            eliminada = pelicula["title"]
            datos.remove(pelicula)
            guardar_datos(datos)
            return {"mensaje": f"*** Película '{eliminada}' BORRADA EXITOSAMENTE. ***"}


# Editar película por título y año
@app.put("/peliculas/{titulo}/{anio}")
def actualizar_pelicula(titulo: str, anio: int, cambios: Pelicula, usuario: str = Depends(verificar_credenciales)):
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
    uvicorn.run("servidor:app", host="0.0.0.0", port=8000, reload=True)