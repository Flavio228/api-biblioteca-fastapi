from fastapi import FastAPI, HTTPException
from database import crear_tabla, insertar_libro, obtener_libros, buscar_libro_id, buscar_libros, marcar_leido, eliminar_libro


from contextlib import asynccontextmanager
from schemas import LibroCrear, LibroRespuesta


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tabla()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/libros", status_code=201, response_model=LibroRespuesta)
def crear_libro(libro: LibroCrear):

    id_libro = insertar_libro(

        libro.titulo,
        libro.autor,
        libro.anio

    )

    return {
        "id": id_libro,
        "titulo": libro.titulo,
        "autor": libro.autor,
        "anio": libro.anio,
        "leido": False
    }

@app.get("/libros", response_model=list[LibroRespuesta])
def listar_libros():
    libros = obtener_libros()
    return libros


@app.get("/libros/buscar", response_model=list[LibroRespuesta])
def buscar_libros_endpoint(texto:str):
    libros = buscar_libros(texto)
    return libros



@app.get("/libros/{id_libro}", response_model=LibroRespuesta)
def obtener_libro_id(id_libro: int): 
    libro = buscar_libro_id(id_libro)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    return libro

@app.put("/libros/{id_libro}/leido", response_model=LibroRespuesta)
def modificar_leido(id_libro:int):
    filas_modificadas = marcar_leido(id_libro)
    if filas_modificadas == 0:
        raise HTTPException (status_code=404, detail="Libro no encontrado")
    libro = buscar_libro_id(id_libro)
    return libro

@app.delete("/libros/{id_libro}")
def borrar_libro(id_libro: int):
    filas_eliminadas = eliminar_libro(id_libro)
    if filas_eliminadas == 0:
        raise HTTPException (status_code=404, detail="Libro no encontrado")
    return {"mensaje": "Libro eliminado correctamente"}


