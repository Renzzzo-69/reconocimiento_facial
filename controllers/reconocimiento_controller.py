from flask import Blueprint, request, jsonify
from services.reconocimiento_service import reconocer
from models.usuario import Usuario
from services.entrenamiento_service import entrenar
from utils.detector_api import cargar_encodings

reco_bp = Blueprint('reco_bp', __name__)

@reco_bp.route("/verificar", methods=["POST"])
def verificar():

    file = request.files["imagen"]
    file_path = "temp.jpg"
    file.save(file_path)

    id_usuario = reconocer(file_path)

    if id_usuario is None:
        # Registrar intento fallido (opcional)
        Usuario.registrar_acceso(None, "NO RECONOCIDO")

        return jsonify({
            "nombre": "DESCONOCIDO",
            "apellidos": "",
            "rol": None
        })

    user = Usuario.obtener_por_id(id_usuario)

    if user is None:
        Usuario.registrar_acceso(None, "NO ENCONTRADO EN BD")
        return jsonify({
            "nombre": "DESCONOCIDO",
            "apellidos": "",
            "rol": None
        })

    # Registrar acceso exitoso
    Usuario.registrar_acceso(id_usuario, "OK")

    return jsonify({
        "id_usuario": user["id_usuario"],
        "nombre": user["nombre"],
        "apellidos": user["apellidos"],
        "rol": user["rol"]
    })

@reco_bp.route("/reentrenar", methods=["POST"])
def reentrenar():
    try:
        entrenar()
        cargar_encodings()   # ← 🔥 recarga el modelo entrenado SIN reiniciar Flask
        return jsonify({
            "ok": True,
            "msg": "Modelo reentrenado y recargado correctamente."
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "msg": str(e)
        }), 500
