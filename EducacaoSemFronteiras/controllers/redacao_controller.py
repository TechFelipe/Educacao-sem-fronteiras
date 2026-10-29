"""Endpoints HTTP de redações e ranking."""
from flask import Blueprint, request, jsonify, session
from flask.views import MethodView
from services.redacao_service import RedacaoService

redacao_bp = Blueprint("redacao", __name__)

class RedacaoController(MethodView):
    """Recebe e valida a estrutura HTTP para cadastrar uma redação."""
    def post(self):
        dados = request.get_json(silent=True) or {}
        # Usa o usuário da sessão quando disponível, evitando confiar só no ID do navegador.
        usuario = session.get("usuario")
        usuario_id = usuario.get("id") if usuario else dados.get("usuario_id")
        try:
            resultado = RedacaoService().criar(usuario_id, dados.get("tema_id"), dados.get("texto"))
            return jsonify({"sucesso": True, "mensagem": "Redação criada com sucesso.", "redacao": resultado}), 201
        except ValueError as erro:
            return jsonify({"sucesso": False, "erro": str(erro)}), 400
        except Exception:
            return jsonify({"sucesso": False, "erro": "Erro ao criar redação. Verifique se o usuário e o tema existem."}), 500

class RankingController(MethodView):
    """Retorna ranking agregado de alunos."""
    def get(self):
        try:
            return jsonify(RedacaoService().ranking()), 200
        except Exception:
            return jsonify({"erro": "Erro ao buscar ranking."}), 500

redacao_bp.add_url_rule("", view_func=RedacaoController.as_view("criar"), methods=["POST"])
redacao_bp.add_url_rule("/ranking", view_func=RankingController.as_view("ranking"), methods=["GET"])
