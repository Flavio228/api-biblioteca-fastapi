# API de Biblioteca con FastAPI

API REST desarrollada con Python, FastAPI, SQLite y Pydantic para gestionar una biblioteca de libros.

El proyecto permite crear, consultar, buscar, actualizar y eliminar libros mediante distintos endpoints HTTP.

Los datos se almacenan de forma persistente con SQLite y la API está desplegada en Railway, por lo que puede utilizarse desde cualquier dispositivo a través de Internet.

## API pública

La API está desplegada en Railway y puede probarse desde la documentación interactiva de Swagger:

https://api-biblioteca-fastapi-production.up.railway.app/docs

## Vista de Swagger
<img width="1900" height="908" alt="Swagger de la API de Biblioteca" src="https://github.com/user-attachments/assets/e1ccf10c-32e2-4841-9659-929d0da1c1df" />


## Funcionalidades

- Crear libros.
- Consultar todos los libros.
- Consultar un libro por ID.
- Buscar libros por título o autor.
- Marcar un libro como leído.
- Eliminar libros.
- Validar los datos de entrada con Pydantic.
- Gestionar errores con respuestas HTTP adecuadas.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/libros` | Crear un libro |
| GET | `/libros` | Obtener todos los libros |
| GET | `/libros/buscar?texto=...` | Buscar libros por título o autor |
| GET | `/libros/{id_libro}` | Obtener un libro por ID |
| PUT | `/libros/{id_libro}/leido` | Marcar un libro como leído |
| DELETE | `/libros/{id_libro}` | Eliminar un libro |

## Validaciones y manejo de errores

La API utiliza Pydantic para validar los datos de entrada antes de guardarlos en la base de datos.

Por ejemplo:

- `titulo` y `autor` deben contener al menos un carácter.
- Se eliminan espacios sobrantes al principio y al final.
- `anio` debe ser mayor que 0 y no puede ser superior al año actual.

Si los datos no son válidos, FastAPI devuelve automáticamente un error `422`.

También se utiliza `HTTPException` para controlar recursos que no existen. Por ejemplo:

```python
if libro is None:
    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )
```

## Persistencia y despliegue

La API utiliza SQLite para almacenar los libros de forma persistente.

En local, la base de datos se guarda en el archivo:

`biblioteca.db`

En Railway, la base de datos se almacena dentro de un volumen persistente para evitar que los datos se pierdan al reiniciar o volver a desplegar la aplicación.

La ruta de la base de datos se construye dinámicamente:

```python
RUTA_BD = os.path.join(
    os.getenv("RAILWAY_VOLUME_MOUNT_PATH", "."),
    "biblioteca.db"
)
```

## Tecnologías utilizadas

- Python
- FastAPI
- Uvicorn
- SQLite
- Pydantic
- Swagger / OpenAPI
- Git y GitHub
- Railway

## Cómo ejecutar el proyecto en local

### 1. Clonar el repositorio

```bash
git clone https://github.com/Flavio228/api-biblioteca-fastapi.git
```
### 2. Entrar en la carpeta del proyecto

```bash
cd api-biblioteca-fastapi
```

### 3. Crear y activar un entorno virtual

En Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 5. Iniciar la API

```bash
uvicorn main:app --reload
```

### 6. Abrir Swagger

```text
http://127.0.0.1:8000/docs
```

## Aprendizajes

Con este proyecto he podido dar un paso más respecto a mi primera API con FastAPI.

He trabajado con una base de datos SQLite para mantener los datos aunque la aplicación se reinicie, he utilizado Pydantic para validar la información que entra en la API y `HTTPException` para gestionar errores como intentar consultar o eliminar un libro que no existe.

También he practicado el uso de path parameters y query parameters, la separación del código entre `main.py`, `database.py` y `schemas.py`, y la refactorización de funciones para evitar repetir lógica.

Por último, he desplegado la API en Railway con un volumen persistente, consiguiendo que pueda utilizarse desde cualquier dispositivo a través de una URL pública.
