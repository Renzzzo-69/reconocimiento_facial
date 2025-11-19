from flask import Blueprint, request, jsonify
from models.usuario import Usuario
import os
import mysql.connector
from config import Config

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route("/usuarios", methods=["GET"])
def listar():
    return jsonify(Usuario.obtener_todos())

@usuario_bp.route("/usuarios", methods=["POST"])
def crear():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    nombre = data.get("nombre")
    if not nombre:
        return jsonify({"error": "El campo 'nombre' es requerido"}), 400
    apellidos = data.get("apellidos")
    if not apellidos:
        return jsonify({"error": "El campo 'apellidos' es requerido"}), 400
    email = data.get("email")
    if not email:
        return jsonify({"error": "El campo 'email' es requerido"}), 400
    rol = data.get("rol")
    if not rol:
        return jsonify({"error": "El campo 'rol' es requerido"}), 400
    
    try:
        uid = Usuario.crear(nombre, apellidos, email, rol)
        return jsonify({"mensaje": "Usuario creado", "id": uid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuario_bp.route("/usuarios/<id_usuario>/capturas", methods=["POST"])
def capturar(id_usuario):
    if 'imagenes' not in request.files:
        return jsonify({"error": "No se encontraron imágenes en la solicitud"}), 400

    imagenes = request.files.getlist('imagenes')
    ruta_capturas = os.path.join('dataset', str(id_usuario))

    if not os.path.exists(ruta_capturas):
        os.makedirs(ruta_capturas)

    for i, imagen in enumerate(imagenes):
        # Asumiendo que las imágenes son jpg y se quieren nombrar de 0.jpg a 89.jpg
        nombre_archivo = f"{i}.jpg"
        imagen.save(os.path.join(ruta_capturas, nombre_archivo))
    
        conn = mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE usuarios SET ruta_dataset=%s WHERE id_usuario=%s",
        (ruta_capturas, id_usuario)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": f"Se guardaron {len(imagenes)} imágenes para el usuario {id_usuario}"})

@usuario_bp.route("/usuarios/<id_usuario>", methods=["PUT"])
def editar(id_usuario):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    nombre = data.get("nombre")
    if not nombre:
        return jsonify({"error": "El campo 'nombre' es requerido"}), 400
    apellidos = data.get("apellidos")
    if not apellidos:
        return jsonify({"error": "El campo 'apellidos' es requerido"}), 400
    email = data.get("email")
    if not email:
        return jsonify({"error": "El campo 'email' es requerido"}), 400
    
    try:
        if Usuario.editar(id_usuario, nombre, apellidos, email) > 0:
            return jsonify({"mensaje": "Usuario actualizado"})
        return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuario_bp.route("/usuarios/<id_usuario>", methods=["DELETE"])
def eliminar(id_usuario):
    try:
        if Usuario.eliminar(id_usuario) > 0:
            return jsonify({"mensaje": "Usuario eliminado"})
        return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
