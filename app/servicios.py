from datetime import datetime
import app.db as db

def crear_nota(titulo, contenido):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.insertar_nota(titulo, contenido, fecha)
    return True

def ver_nota(id_nota):
    return db.obtener_nota_por_id(id_nota)

def editar_nota(id_nota, titulo, contenido):
    filas = db.actualizar_nota(id_nota, titulo, contenido)
    return filas > 0

def borrar_nota(id_nota):
    filas = db.eliminar_nota(id_nota)
    return filas > 0

def completar_nota(id_nota):
    filas = db.marcar_completada(id_nota)
    return filas > 0

def obtener_notas_avanzado(completada, buscar, limit, offset, orden):
    return db.obtener_notas_avanzado(completada, buscar, limit, offset, orden)

def contar_notas(completada, buscar):
    return db.contar_notas(completada, buscar)