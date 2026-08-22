from flask import Blueprint, request, jsonify
from services.tema_service import TemaService

tema_bp = Blueprint("tema", __name__)
service = TemaService()

@tema_bp.route("/buscar", methods=["GET"])
def buscar():
    termo = request.args.get("termo")
    dificuldade = request.args.get("dificuldade")
    return jsonify(service.buscar(termo, dificuldade))
