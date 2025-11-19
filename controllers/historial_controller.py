from flask import Blueprint, jsonify, request
from models.usuario import Usuario

historial_bp = Blueprint('historial_bp', __name__)

@historial_bp.route("/historial/<int:id_usuario>", methods=["GET"])
def historial(id_usuario):
    historial = Usuario.obtener_historial(id_usuario)
    return jsonify(historial)
