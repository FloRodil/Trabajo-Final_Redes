from fastapi import FastAPI, HTTPException, Depends, status #1-12 se agregó Depends y status
from fastapi.security import HTTPBasic, HTTPBasicCredentials #1-12 se agregó
from typing import Optional, Dict #1-12 se agregó Dict
from pydantic import BaseModel # valida, convierte y estructura datos JSON -> en objeto de la clase y el objeto en diccionario
import json
import uvicorn
import secrets #1-12 se agregó

archivo_datos = "movies.json"

app = FastAPI()

# Cargar datos
def cargar_datos():
    with open(archivo_datos, "r", encoding="utf-8") as a:
        #print(type(json.load(a)))
        return json.load(a)

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
    thumbnail_width: Optional[int] = 320
    thumbnail_height: Optional[int] = 320

# -------Agregado 1-12 -------------------------------------------------------

# HTTPBasic() dependencia de Fastapli que detecta si 
# el request trae el encabezado HTTP Authorization: Basic <credenciales_base64>
# Decodifica ese Base64 y obtiene username y password

security = HTTPBasic() 

USUARIOS: Dict[str, str] = {
    "ivan": "ivan123",
    "user": "user_1" 
}

# Autentificación de usuarios
def verificar_credenciales(credenciales: HTTPBasicCredentials = Depends(security)) -> str: #Depends(security), llama a HTTPBasic() y pasa credenciales a la función
    pwd_correcta = USUARIOS.get(credenciales.username)
    if not pwd_correcta or not secrets.compare_digest(credenciales.password, pwd_correcta): #secrets.compare_digest() compara strings sin dar pistas de duración.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credenciales.username  # Devuelve el nombre del usuario autenticado

#-------------------------------------------------------------------------------

# Obtener todas las películas
@app.get("/peliculas")
def mostrar_peliculas():
    return cargar_datos()

# Obtener una película por su título
@app.get("/peliculas/{pelicula_titulo}")
def mostrar_pelicula(pelicula_titulo: str):
    datos = cargar_datos()
    for pelicula in datos:
        if pelicula["title"] == pelicula_titulo:
            return pelicula
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No encontrado")

# Agregar una nueva película
@app.post("/peliculas")
def agregar_pelicula(pelicula: Pelicula, usuario: str = Depends(verificar_credenciales)):
    datos = cargar_datos()
    datos.append(pelicula.model_dump()) # el método model.dump() es necesario para transformar el objeto película en un diccionario
    guardar_datos(datos)
    return{"mensaje": "Película agregada", "Película": pelicula}

# Borrar película por título
@app.delete("/peliculas")
def borrar_pelicula(pelicula_titulo: str, usuario: str = Depends(verificar_credenciales)):
    datos = cargar_datos()
    for pelicula in datos:
        if pelicula["title"] == pelicula_titulo:
            datos.remove(pelicula)
            guardar_datos(datos)
        return{"mensaje": "Película borrada", "Título": pelicula_titulo}

if __name__=="__main__":
    #cargar_datos()
    uvicorn.run("servidor:app", host="0.0.0.0", port=8000, reload=True)