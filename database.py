import sqlite3
import os

RUTA_BD = os.path.join(
    os.getenv("RAILWAY_VOLUME_MOUNT_PATH", "."),
    "biblioteca.db"
)

def formatear_libro(libro):
    libro_diccionario = {
        "id" : libro [0],
        "titulo" : libro [1],
        "autor" : libro [2],
        "anio" : libro [3],
        "leido" : bool(libro[4])
    }
    return libro_diccionario

def crear_tabla():

    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()


    cursor.execute ("""
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        anio INTEGER,
        leido INTEGER DEFAULT 0)
        
    """)
    conexion.commit()
    conexion.close()    

def insertar_libro(titulo, autor, anio):


    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()
    cursor.execute(
        """
        INSERT INTO libros (titulo, autor, anio)
        VALUES(?,?,?)
    """, (titulo, autor, anio)
    )

    id_libro = cursor.lastrowid
    conexion.commit()
    conexion.close()

    return id_libro

def obtener_libros():
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT * FROM libros        
        """
    )
    libros = cursor.fetchall()
    libros_formateados = []
    for libro in libros:
        libro_diccionario = formatear_libro(libro)
        libros_formateados.append(libro_diccionario)

    conexion.close()
    return libros_formateados

def buscar_libro_id (id_libro):
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT * FROM libros
        WHERE id = ?
        """,(id_libro,)
    )

    libro = cursor.fetchone()

    conexion.close()
    if libro is None:
        return None 
    
    libro_diccionario = formatear_libro(libro)   

    return libro_diccionario

def buscar_libros(texto):
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()
    patron = f"%{texto}%"
    cursor.execute(
        """
        SELECT * FROM libros
        WHERE titulo LIKE ? OR autor LIKE ?
        """, (patron, patron)

    )
    libros = cursor.fetchall()
    libros_formateados = []
    for libro in libros:
        libro_diccionario = formatear_libro(libro)
        libros_formateados.append(libro_diccionario)
    conexion.close()
    return  libros_formateados

def marcar_leido(id_libro):
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE libros
        SET leido = 1
        WHERE id = ?

        """, (id_libro,)
    )
    conexion.commit()
    filas_modificadas = cursor.rowcount 
    conexion.close()
    return filas_modificadas

def eliminar_libro(id_libro):
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM libros
        WHERE id = ?

        """, (id_libro,)
    )
    conexion.commit()
    filas_eliminadas = cursor.rowcount
    conexion.close()
    return filas_eliminadas






