from fastapi import FastAPI, HTTPException,status
from typing import Optional
from pydantic import BaseModel
import json
import uvicorn

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

# Obtener todas las películas
@app.get("/peliculas")
def mostrar_peliculas():
    return cargar_datos()

# Obtener una película por su título <<< MODIFICADO
@app.get("/peliculas/{pelicula_titulo}")
def mostrar_pelicula(pelicula_titulo: str):
    datos = cargar_datos()
    coincidencias = []

    for pelicula in datos:
        if pelicula["title"].lower() == pelicula_titulo.lower():
            margen = 6*" "

            texto = (
                4* " " + f"{'-'*55}\n"
                + margen + f"Título: {pelicula['title']}\n"
                + margen + f"Año: {pelicula['year']}\n"
                + margen + f"Géneros: {', '.join(pelicula['genres']) if pelicula['genres'] else '\033[3mNo disponible\033[0m'}\n"
                + margen + f"Elenco: {', '.join(pelicula['cast']) if pelicula['cast'] else '\033[3mNo disponible\033[0m'}\n"
                + margen + f"Href: {pelicula['href'] if pelicula['href'] else '\033[3mNo disponible\033[0m'}\n"
                + 4* " " + f"{'-'*55}\n"
            )

            coincidencias.append(texto)

    if coincidencias:
        return "\n".join(coincidencias)

    raise HTTPException(status_code=404, detail="No encontrado")

# @app.get("/peliculas/{pelicula_titulo}")
# def mostrar_pelicula(pelicula_titulo: str):
#     datos = cargar_datos()
#     for pelicula in datos:
#         if pelicula["title"] == pelicula_titulo:
#             return pelicula
#     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No encontrado")


# Agregar una nueva película
@app.post("/peliculas")
def agregar_pelicula(pelicula: Pelicula):
    datos = cargar_datos()
    datos.append(pelicula.model_dump()) # el método model.dump() es necesario para transformar el objeto película en un diccionario
    guardar_datos(datos)
    return{"mensaje": "Película agregada", "Película": pelicula}

# Borrar película por título
@app.delete("/peliculas")
def borrar_pelicula(pelicula_titulo: str):
    datos = cargar_datos()
    for pelicula in datos:
        if pelicula["title"] == pelicula_titulo:
            datos.remove(pelicula)
            guardar_datos(datos)
        return{"mensaje": "Película borrada", "Título": pelicula_titulo}

if __name__=="__main__":
    #cargar_datos()
    uvicorn.run("servidor:app", host="0.0.0.0", port=8000, reload=True)