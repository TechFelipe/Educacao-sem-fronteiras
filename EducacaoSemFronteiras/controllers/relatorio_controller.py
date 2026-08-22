from flask import Blueprint, jsonify
from services.relatorio_service import RelatorioService

relatorio_bp = Blueprint("relatorio", __name__)
service = RelatorioService()

@relatorio_bp.route("/<int:usuario_id>/relatorio", methods=["GET"])
def relatorio(usuario_id):
    return jsonify(service.relatorio(usuario_id))

@relatorio_bp.route("/<int:usuario_id>/evolucao", methods=["GET"])
def evolucao(usuario_id):
    return jsonify(service.evolucao(usuario_id))

@relatorio_bp.route("/<int:usuario_id>/competencia-fraca", methods=["GET"])
def competencia_fraca(usuario_id):
    return jsonify(service.competencia_fraca(usuario_id))
