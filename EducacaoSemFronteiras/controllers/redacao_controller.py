from flask import Blueprint, request, jsonify
from services.redacao_service import RedacaoService

redacao_bp = Blueprint("redacao", __name__)
service = RedacaoService()

@redacao_bp.route("", methods=["POST"])
def criar():
    try:
        dados = request.get_json() or {}
        resultado = service.criar(
            dados.get("usuario_id"),
            dados.get("tema_id"),
            dados.get("texto")
        )
        return jsonify(resultado), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@redacao_bp.route("/ranking", methods=["GET"])
def ranking():
    return jsonify(service.ranking())
