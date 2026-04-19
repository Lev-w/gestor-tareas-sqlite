import sqlite3

DB_NAME = "notas.db"

def conectar():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    return con

def crear_tabla():
    with conectar() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo           TEXT         NOT NULL,
                contenido        TEXT         NOT NULL,
                fecha_creacion   DATETIME     DEFAULT CURRENT_TIMESTAMP,
                completada       INTEGER DEFAULT 0
            )
        """)

def marcar_completada(id_nota):
    with conectar() as con:
        cursor = con.execute(
            "UPDATE notas SET completada = 1 WHERE id = ?",
            (id_nota,)
        )
        return cursor.rowcount

def insertar_nota(titulo, contenido, fecha):
    with conectar() as con:
        con.execute(
            "INSERT INTO notas (titulo, contenido, fecha_creacion) VALUES (?, ?, ?)",
            (titulo, contenido, fecha)
        )

def obtener_nota_por_id(id_nota):
    with conectar() as con:
        return con.execute(
            "SELECT * FROM notas WHERE id = ?",
            (id_nota,)
        ).fetchone()

def actualizar_nota(id_nota, titulo, contenido):
    with conectar() as con:
        cursor = con.execute(
            "UPDATE notas SET titulo = ?, contenido = ? WHERE id = ?",
            (titulo, contenido, id_nota)
        )
        return cursor.rowcount

def eliminar_nota(id_nota):
    with conectar() as con:
        cursor = con.execute(
            "DELETE FROM notas WHERE id = ?",
            (id_nota,)
        )
        return cursor.rowcount
    
def obtener_notas_avanzado(completada, buscar, limit, offset, orden):
    with conectar() as con:
        query = "SELECT * FROM notas"
        condiciones = []
        valores = []
        if completada is not None:
            condiciones.append("completada = ?")
            valores.append(completada)
        if buscar:
            buscar = buscar.lower().strip()
            condiciones.append("(LOWER(titulo) LIKE ? OR LOWER(contenido) LIKE ?)")
            valores.append(f"%{buscar}%")
            valores.append(f"%{buscar}%")
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        query += f" ORDER BY {orden} DESC"
        query += " LIMIT ? OFFSET ?"
        valores.append(limit)
        valores.append(offset)
        return con.execute(query, valores).fetchall()
    
def contar_notas(completada, buscar):
    with conectar() as con:
        query = "SELECT COUNT(*) FROM notas"
        condiciones = []
        valores = []
        if completada is not None:
            condiciones.append("completada = ?")
            valores.append(completada)
        if buscar:
            buscar = buscar.lower().strip()
            condiciones.append("(LOWER(titulo) LIKE ? OR LOWER(contenido) LIKE ?)")
            valores.append(f"%{buscar}%")
            valores.append(f"%{buscar}%")
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        return con.execute(query, valores).fetchone()[0]