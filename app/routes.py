from flask import Flask, request, jsonify, Blueprint
import app.servicios as servicios
import app.db as db

main = Blueprint("main", __name__)

db.crear_tabla()

@main.route("/notas", methods=["GET"])
def obtener_notas():
    completadas = request.args.get("completadas")
    buscar = request.args.get("buscar")
    page = request.args.get("page")
    limit = request.args.get("limit")
    orden = request.args.get("orden")
    
    completada = None
    
    if completadas == "true":
        completada = 1
    elif completadas == "false":
        completada = 0
    elif completadas is not None:
        return jsonify({"error": "Datos incorrectos"}), 400
    
    try:
        page = int(page) 
        if page < 1:
            page = 1
    except:
        page = 1

    try:
        limit = int(limit)
        if limit > 50:
            limit = 50
        if limit < 1:
            limit = 5
    except:
        limit = 5

    offset = (page - 1) * limit
    
    notas = servicios.obtener_notas_avanzado(completada, buscar, limit, offset, orden)
    total = servicios.contar_notas(completada, buscar)

    total_pages = (total + limit - 1) // limit

    resultado = servicios.serializar_notas(notas)

    return jsonify({
        "page": page,
        "total_pages": total_pages,
        "limit": limit,
        "total": total,
        "data": resultado
    })

@main.route("/notas", methods=["POST"])
def crear_nota():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Se requiere JSON"}), 400

    titulo = data.get("titulo")
    contenido = data.get("contenido")

    if not titulo or not titulo.strip():
        return jsonify({"error": "El titulo es obligatorio"}), 400
    
    if not contenido or not contenido.strip():
        return jsonify({"error": "El contenido es obligatorio"}), 400
    
    titulo = titulo.strip()
    contenido = contenido.strip()

    servicios.crear_nota(titulo, contenido)

    return jsonify({"mensaje": "Nota creada"})

@main.route("/notas/<int:id_nota>", methods=["GET"])
def obtener_nota(id_nota):
    nota = servicios.ver_nota(id_nota)

    if nota is None:
        return jsonify({"error": "No encontrada"}), 404
    
    return jsonify({
        "id": nota[0],
        "titulo": nota[1],
        "contenido": nota[2],
        "fecha": nota[3],
        "completada": nota[4]
    })

@main.route("/notas/<int:id_nota>", methods=["PUT"])
def editar_nota(id_nota):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Se requiere JSON"}), 400
    
    titulo = data.get("titulo")
    contenido = data.get("contenido")

    if titulo is None and contenido is None:
        return jsonify({"error": "Debe actualizar al menos un campo"}), 400
    
    if titulo is not None:
        if not titulo.strip() or not isinstance(titulo, str):
            return jsonify({"error": "El titulo debe ser texto valido"}), 400
        titulo = titulo.strip()
        
    if contenido is not None:
        if not contenido.strip() or not isinstance(titulo, str):
            return jsonify({"error": "El contenido debe ser texto valido"}), 400
        contenido = contenido.strip()

    ok = servicios.editar_nota(id_nota, titulo, contenido)

    if not ok:
        return jsonify({"error": "No existe"}), 404
    
    return jsonify({"mensaje": "Actualizada"}), 200

@main.route("/notas/<int:id_nota>", methods=["DELETE"])
def eliminar_nota(id_nota):
    ok = servicios.borrar_nota(id_nota)

    if not ok:
        return jsonify({"error": "No existe"}), 404
    
    return jsonify({"mensaje": "Eliminada"})

@main.route("/notas/<int:id_nota>/completar", methods=["PUT"])
def completar_nota(id_nota):
    ok = servicios.completar_nota(id_nota)

    if not ok:
        return jsonify({"error": "No existe"}), 404

    return jsonify({"mensaje": "Nota completada"})